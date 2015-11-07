#!/usr/bin/env python

from spf.mr.language.type_.array_type import ArrayType
from spf.mr.language.type_.term_type import TermType
from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType, Option
from spf.utils.lisp_reader import LispReader

import re
from StringIO import StringIO

class TypeRepository(object):
  ENTITY_TYPE_NAME = 'e'
  INDEX_TYPE_NAME = 'ind'
  TRUTH_VALUE_TYPE_NAME = 't'

  def __init__(self_, types_file_):
    self_.types_ = {}
    self_.index_type_ = TermType(TypeRepository.INDEX_TYPE_NAME)
    self_.truth_value_type_ = TermType(TypeRepository.TRUTH_VALUE_TYPE_NAME)
    self_.entity_type_ = TermType(TypeRepository.ENTITY_TYPE_NAME)

    self_.add_type(self_.index_type_)
    self_.add_type(self_.truth_value_type_)
    self_.add_type(self_.entity_type_)
    # self_.get_array_type_created_if_needed(self_.entity_type_)

    if types_file_ is not None:
      stripped_file = ''
      for line in open(types_file_, 'r'):
        line = line.strip()
        line = re.split('\\s*//', line)[0]
        if len(line) != 0:
          stripped_file += line + ' '
      lisp_reader = LispReader(StringIO(stripped_file))
      while lisp_reader.has_next():
        self_.add_type(self_.create_type_from_string(lisp_reader.next()))

  def generalize_type(self_, type_):
    if type_.is_complex():
      recursive_domain_ = isinstance(type_, RecursiveComplexType)
      option_ = type_.get_option() if recursive_domain_ else None
      return self_.get_type_create_if_needed(
          self_.generalize_type(type_.get_final_range() if recursive_domain_ else type_.get_range()),
          self_.generalize_type(type_.get_domain()),
          option_)
    elif isinstance(type_, TermType):
      current_type_ = type_
      super_type_ = current_type_.get_parent()
      while super_type_ is not None:
        current_type_ = super_type_
      return current_type_
    if type_.is_array():
      return self_.get_array_type_created_if_needed(type_.get_base_type())
    else:
      raise RuntimeError('Unhandled Type type: %s' % type_.__class__.__name__)

  def get_array_type_created_if_needed(self_, base_type_):
    return self_.get_type_create_if_needed(base_type_.get_name() +ArrayType.ARRAY_SUFFIX)

  def get_entity_type(self_):
    return self_.entity_type_

  def get_index_predicate_type_for_array(self_, array_type_):
    base_type_ = array_type_.get_base_type()
    return self_.get_type_create_if_needed(
        self_.get_type_create_if_needed(base_type_, self_.index_type_),
        array_type_)

  def get_index_type(self_):
    return self_.index_type_

  def get_truth_value_type(self_):
    return self_.truth_value_type_

  def get_type(self_, name_):
    return self_.types_.get(name_, None)

  def get_type_create_if_needed(self_, *args):
    if len(args) == 1 and isinstance(args[0], str):
      label_ = args[0]
      existing_type = self_.get_type(label_)
      if existing_type is None:
        if (label_.startswith(ComplexType.COMPLEX_TYPE_OPEN_PAREN) and
            label_.endswith(ComplexType.COMPLEX_TYPE_CLOSE_PAREN)):
          return self_.add_type(self_.create_complex_type_from_string(label_))
        elif label_.endswith(ArrayType.ARRAY_SUFFIX):
          return self_.add_type(self_.create_array_type_from_string(label_))
      return existing_type
    elif (len(args) == 3 and
        isinstance(args[0], Type) and
        isinstance(args[1], Type) and
        (args[2] is None or isinstance(args[2], Option))):
      return self_.get_type_create_if_needed(
          ComplexType.compose_string(args[0], args[1], args[2]))
    else:
      raise NameError('Wrong arguments for get_type_create_if_needed')

  def __str__(self_):
    ret = ''
    for key, value in self_.types_.iteritems():
      ret += key
      ret += '\t::\t'
      ret += repr(value)
      ret += '\n'
    return ret

  def add_type(self_, type_):
    if type_.get_name() in self_.types_:
      return self_.get_type(type_.get_name())
    self_.types_.update({type_.get_name(): type_})
    if type_.is_array():
      self_.create_and_add_array_acces_types(type_)
    return type_

  def create_and_add_array_acces_types(self_, array_type_):
    self_.get_index_predicate_type_for_array(array_type_)
    self_.get_sub_predicate_type_for_array(array_type_)

  def create_array_type_from_string(self_, string_):
    return ArrayType(string_,
        self_.get_type_create_if_needed(string_[:len(string_) - len(ArrayType.ARRAY_SUFFIX)]),
        self_.entity_type_)

  def create_complex_type_from_string(self_, string_):
    inner_string = string_[1:-1].strip()
    parenthesis_counter = 0
    i = 0
    while i < len(inner_string):
      c = inner_string[i]
      if (c == ComplexType.COMPLEX_TYPE_SEP and parenthesis_counter == 0):
        break
      i += 1
      if c == ComplexType.COMPLEX_TYPE_OPEN_PAREN:
        parenthesis_counter += 1
      elif c == ComplexType.COMPLEX_TYPE_CLOSE_PAREN:
        parenthesis_counter -= 1
    i += 1
    range_string_ = inner_string[i:].strip()
    domain_string_ = inner_string[:i].strip()

    domain_string_trimmed, option_ = Option.parse(domain_string_)
    domain_ = self_.get_type_create_if_needed(domain_string_trimmed)
    range_ = self_.get_type_create_if_needed(range_string_)

    return ComplexType.create(string_, domain_, range_, option_)

  def create_term_type_from_string(self_, string_):
    lisp_reader = LispReader(StringIO(string_))
    label_ = lisp_reader.next()
    parent_type_string_ = lisp_reader.next()
    parent_type_ = self_.get_type(parent_type_string_)
    if isinstance(parent_type_, TermType):
      return TermType(label_, parent_type_)
    else:
      raise NameError(
          'Parent (%s) of primitive type (%s) must be a primitive type'% (
            parent_type_, label_))

  def create_type_from_string(self_, string_):
    if string_.endswith(ArrayType.ARRAY_SUFFIX):
      return self_.create_array_type_from_string(string_)
    elif string_.startswith('('):
      return self_.create_term_type_from_string(string_)
    elif (string_.startswith(ComplexType.COMPLEX_TYPE_OPEN_PAREN) and
        string_.endswith(ComplexType.COMPLEX_TYPE_CLOSE_PAREN)):
      return self_.create_complex_type_from_string(string_)
    else:
      return TermType(string_)
