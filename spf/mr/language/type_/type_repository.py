#!/usr/bin/env python

from spf.mr.language.type_.array_type import ArrayType
from spf.mr.language.type_.complex_type_builder import ComplexTypeBuilder
from spf.mr.language.type_.term_type import TermType
from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType, Option
from spf.mr.language.type_.api import Type
from spf.utils.lisp_reader import LispReader
import re
from StringIO import StringIO


class TypeRepository(object):
    """ TypeRepository is an facility for creating and storing type. """
    ENTITY_TYPE_NAME = 'e'
    INDEX_TYPE_NAME = 'ind'
    TRUTH_VALUE_TYPE_NAME = 't'

    def __init__(self, types_file):
        """

        :param types_file:
        :type types_file: str
        :return:
        """
        self.types = {}
        self.index_type = TermType(self.INDEX_TYPE_NAME)
        self.truth_value_type = TermType(self.TRUTH_VALUE_TYPE_NAME)
        self.entity_type = TermType(self.ENTITY_TYPE_NAME)

        self.add_type(self.index_type)
        self.add_type(self.truth_value_type)
        self.add_type(self.entity_type)
        # self.get_array_type_created_if_needed(self.entity_type_)

        if types_file is not None:
            try:
                stripped_file = ""
                try:
                    for line in open(types_file, 'r'):
                        line = line.strip()
                        line = re.split('\\s*//', line)[0]
                        if len(line) != 0:
                            stripped_file += line + ' '
                    lisp_reader = LispReader(StringIO(stripped_file))
                except Exception, e:
                    raise Exception(e)
                while lisp_reader.has_next():
                    self.add_type(self.create_type_from_string(lisp_reader.next()))
            except IOError, e:
                raise AttributeError(e)

        self.lock_primitives = True

    def generalize_type(self, type_):
        """
        Generalize type to its most superterm. Supposing we have an ontology like ((lo e)), for an input TermType lo,
        the return value should be e.

        :param type_:
        :return:
        """
        if type_.is_complex():
            recursive_domain_ = isinstance(type_, RecursiveComplexType)
            option_ = type_.get_option() if recursive_domain_ else None
            return self.get_type_create_if_needed(
                self.generalize_type(type_.get_final_range() if recursive_domain_ else type_.get_range()),
                self.generalize_type(type_.get_domain()),
                option_)
        elif isinstance(type_, TermType):
            current_type = type_
            super_type = current_type.get_parent()
            while super_type is not None:
                current_type = super_type
                super_type = current_type.get_parent()
            return current_type
        if type_.is_array():
            return self.get_array_type_created_if_needed(type_.get_base_type())
        else:
            raise RuntimeError('Unhandled Type type: %s' % type_.__class__.__name__)

    def get_array_type_created_if_needed(self, base_type_):
        return self.get_type_create_if_needed(base_type_.get_name() + ArrayType.ARRAY_SUFFIX)

    def get_entity_type(self):
        return self.entity_type

    def get_index_predicate_type_for_array(self, array_type):
        base_type = array_type.get_base_type()
        return self.get_type_create_if_needed(self.get_type_create_if_needed(base_type, self.index_type), array_type)

    def get_index_type(self):
        return self.index_type

    def get_truth_value_type(self):
        return self.truth_value_type

    def get_type(self, name):
        return self.types.get(name, None)

    def get_type_create_if_needed(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            label = args[0]
            existing_type = self.get_type(label)
            if existing_type is None:
                if label.startswith(ComplexType.COMPLEX_TYPE_OPEN_PAREN) and\
                        label.endswith(ComplexType.COMPLEX_TYPE_CLOSE_PAREN):
                    return self.add_type(self.create_complex_type_from_string(label))
                elif label.endswith(ArrayType.ARRAY_SUFFIX):
                    return self.add_type(self.create_array_type_from_string(label))
            return existing_type
        elif len(args) == 2 and isinstance(args[0], Type) and isinstance(args[1], Type):
            return self.get_type_create_if_needed(
                ComplexType.compose_string(args[0], args[1], None))
        elif len(args) == 3 and isinstance(args[0], Type) and isinstance(args[1], Type) and\
                (args[2] is None or isinstance(args[2], Option)):
            return self.get_type_create_if_needed(
                ComplexType.compose_string(args[0], args[1], args[2]))
        else:
            raise NameError('Wrong arguments for get_type_create_if_needed')

    def __str__(self):
        ret = ''
        for key, value in self.types.iteritems():
            ret += key
            ret += '\t::\t'
            ret += repr(value)
            ret += '\n'
        return ret

    def add_type(self, type_):
        if type_.get_name() in self.types:
            return self.get_type(type_.get_name())
        self.types.update({type_.get_name(): type_})
        if type_.is_array():
            self.create_and_add_array_access_types(type_)
        return type_

    def create_and_add_array_access_types(self, array_type):
        #self.get_index_predicate_type_for_array(array_type)
        #self.get_sub_predicate_type_for_array(array_type)
        pass

    def create_array_type_from_string(self, string):
        return ArrayType(string,
                         self.get_type_create_if_needed(string[:len(string) - len(ArrayType.ARRAY_SUFFIX)]),
                         self.entity_type)

    def create_complex_type_from_string(self, string):
        inner_string = string[1:-1].strip()
        parenthesis_counter = 0
        i = 0
        while i < len(inner_string):
            c = inner_string[i]
            if c == ComplexType.COMPLEX_TYPE_SEP and parenthesis_counter == 0:
                break
            i += 1
            if c == ComplexType.COMPLEX_TYPE_OPEN_PAREN:
                parenthesis_counter += 1
            elif c == ComplexType.COMPLEX_TYPE_CLOSE_PAREN:
                parenthesis_counter -= 1
        i += 1
        range_string = inner_string[i:].strip()
        domain_string = inner_string[:i - 1].strip()

        domain_stringtrimmed, option = Option.parse(domain_string)
        domain = self.get_type_create_if_needed(domain_stringtrimmed)
        range_ = self.get_type_create_if_needed(range_string)

        return ComplexTypeBuilder.create(string, domain, range_, option)

    def create_term_type_from_string(self, string):
        lisp_reader = LispReader(StringIO(string))
        label_ = lisp_reader.next()
        parent_typestring = lisp_reader.next()
        parent_type = self.get_type(parent_typestring)
        if isinstance(parent_type, TermType):
            return TermType(label_, parent_type)
        else:
            raise NameError(
                'Parent (%s) of primitive type (%s) must be a primitive type' % (
                    parent_type, label_))

    def create_type_from_string(self, string):
        if string.endswith(ArrayType.ARRAY_SUFFIX):
            return self.create_array_type_from_string(string)
        elif string.startswith('('):
            return self.create_term_type_from_string(string)
        elif (string.startswith(ComplexType.COMPLEX_TYPE_OPEN_PAREN) and
                  string.endswith(ComplexType.COMPLEX_TYPE_CLOSE_PAREN)):
            return self.create_complex_type_from_string(string)
        else:
            return TermType(string)
