#!/usr/bin/env python
from spf.mr.lambda_.term import Term
from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
import logging
import re


class LogicalConstant(Term):
    LOG = logging.getLogger(__name__)

    DYNAMIC_MARKER = '@'
    ILLEGAL_CHARS = '(),:#'
    ILLEGAL_PREFIX_CHARS = ILLEGAL_CHARS + '!$@'
    REGEXP_NAME_PATTERN = re.compile('(?:%s[^%s]+)|(?:[^%s][^%s]*)' % (
        DYNAMIC_MARKER, ILLEGAL_CHARS, ILLEGAL_PREFIX_CHARS, ILLEGAL_CHARS))

    def __init__(self, name, type_):
        super(LogicalConstant, self).__init__(type_)
        self.name = name

    def accept(self, visitor):
        visitor.visit(self)

    def calculate_hash_code(self):
        return (31 * super(LogicalConstant, self).calculate_hash_code() +
                (0 if self.name is None else hash(self.name)))

    def get_base_name(self):
        sep = len(self.name) - len(self.get_type().get_name()) - len(Term.TYPE_SEPARATOR)
        return self.name[:sep]

    def get_name(self):
        return self.name

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other, mapping=None):
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices
        if LogicLanguageServices.get_ontology() is None:
            return isinstance(other, LogicalConstant) and self.do_equals(other)
        else:
            return id(self) == id(other)

    def do_equals(self, other, mapping=None):
        if id(self) == id(other):
            return True
        if not super(LogicalConstant, self).do_equals(other):
            return False
        if self.name is None:
            if other.name is not None:
                return False
        elif other.name != self.name:
            return False
        return True

    @staticmethod
    def create(name, type_, dynamic=False):
        if name.startswith(LogicalConstant.DYNAMIC_MARKER):
            name = name[len(LogicalConstant.DYNAMIC_MARKER):]
            dynamic = True

        from spf.mr.lambda_.logic_language_services import LogicLanguageServices
        ontology = LogicLanguageServices.get_ontology()
        if ontology is None:
            return LogicalConstant(name, type_)
        else:
            return ontology.get_or_add(LogicalConstant(name, type_), dynamic)

    @staticmethod
    def create_dynamic(name, type_):
        """
        :param name:
        :param type_:
        :rtype: object
        """
        return LogicalConstant.create(name, type_, True)

    @classmethod
    def escape_string(cls, string):
        first = True
        output = ''
        for c in string:
            if c in cls.DYNAMIC_MARKER:
                if (first and len(string) > 1) or not first:
                    output += c
                else:
                    output += '_I%d_' % ord(c)
            elif first and c in cls.ILLEGAL_PREFIX_CHARS:
                output += '_I%d_' % ord(c)
            elif c in cls.ILLEGAL_CHARS:
                output += '_I%d_' % ord(c)
            elif c.isspace():
                output += '_I%d_' % ord(c)
            else:
                output += c
            first = False
        return output

    @classmethod
    def is_valid_name(cls, name):
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices
        split = name.split(':', 2)
        type_repository = LogicLanguageServices.get_type_repository()
        return cls.REGEXP_NAME_PATTERN.match(split[0]) is not None and \
               type_repository.get_type_create_if_needed(split[1]) is not None

    @staticmethod
    def make_name(name, type_):
        return '%s:%s' % (name, str(type_))

    @staticmethod
    def read(string, type_repository=None):
        if type_repository is None:
            from spf.mr.lambda_.logic_language_services import LogicLanguageServices
            type_repository = LogicLanguageServices.get_type_repository()

        split = string.split(Term.TYPE_SEPARATOR)
        if len(split) != 2:
            raise LogicalExpressionRuntimeError('Constant syntax error: %s' % string)
        type_ = type_repository.get_type(split[1])
        if type_ is None:
            type_ = type_repository.get_type_create_if_needed(split[1])
        if type_ is None:
            raise LogicalExpressionRuntimeError('Unknown type for: %s' % string)
        return LogicalConstant.create(string, type_)

    class Reader(LogicalExpression.Reader):
        @staticmethod
        def is_valid(string):
            return LogicalConstant.is_valid_name(string)

        @staticmethod
        def read(string, mapping, type_repository, type_comparator, reader):
            return LogicalConstant.read(string, type_repository)


class WrappedConstant(object):
    def __init__(self, constant):
        self.constant = constant

    def __eq__(self, other):
        return isinstance(other, WrappedConstant) and self.constant.do_equals(other.constant)

    def __hash__(self):
        return hash(self.constant)
