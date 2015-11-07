#!/usr/bin/env python

from spf.mr.lambda_.term import Term
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

  def __init__(self_, name_, type_):
    super(LogicalConstant, self_).__init__(type_)
    self_.name_ = name_

  def accept(self_, visitor):
    visitor.visit(self_)

  def calculate_hash_code(self_):
    return (31 * super(LogicalConstant, self_).calculate_hash_code() +
        (0 if self_.name_ is None else hash(self_.name_)))

  def get_base_name(self_):
    sep = len(self_.name_) - len(self_.get_type().get_name()) - len(Term.TYPE_SEPARATOR)
    return self_.name_[:sep]

  def get_name(self_):
    return self_.name_

  def equals(self_, other, mapping=None):
    if LogicLanguageServices.get_ontology() is None:
      return isinstance(other, LogicalConstant) and self_.do_equals(other)
    else:
      return id(self_) == id(other)

  def do_equals(self_, other, mapping=None):
    if id(self_) == id(other):
      return True
    if not super(LogicalConstant, self_).do_equals(other):
      return False
    if self_.name_ is None:
      if other.name_ is not None:
        return False
    elif not self_.name_ == other.name_:
      return False
    return True

  @staticmethod
  def create(name_, type_, dynamic=False):
    if name_.startswith(LogicalConstant.DYNAMIC_MARKER):
      name_ = name_[len(LogicalConstant.DYNAMIC_MARKER):]
      dynamic = True

    from spf.mr.lambda_.logic_language_services import LogicLanguageServices
    ontology_ = LogicLanguageServices.get_ontology()
    if ontology_ is None:
      return LogicalConstant(name_, type_)
    else:
      return ontology_.get_or_add(LogicalConstant(name_, type_), dynamic)

  @staticmethod
  def create_dynamic(name_, type_):
    return LogicalConstant.create(name_, type_, True)

  @staticmethod
  def escape_string(string_):
    first = True
    output = ''
    for c in string_:
      if c in LogicalConstant.DYNAMIC_MARKER:
        if (first and len(string_) > 1) or not first:
          output += c
        else:
          output += '_I%d_' % ord(c)
      elif first and c in LogicalConstant.ILLEGAL_PREFIX_CHARS:
        output += '_I%d_' % ord(c)
      elif c in LogicalConstant.ILLEGAL_CHARS:
        output += '_I%d_' % ord(c)
      elif c.isspace():
        output += '_I%d_' % ord(c)
      else:
        output += c
      first = False
    return output

  @staticmethod
  def is_valid_name(name_):
    from spf.mr.lambda_.logic_language_services import LogicLanguageServices
    split = name_.split(':', 2)
    type_repository_ = LogicLanguageServices.get_type_repository()
    return ((REGEXP_NAME_PATTERN.matches(split[0]) is not None) and
        (type_repository_.get_type_create_if_needed(split[1]) is not None))

  @staticmethod
  def make_name(name_, type_):
    return '%s:%s'% (name_, str(type_))

  @staticmethod
  def read(string_, type_repository_=None):
    if type_repository_ is None:
      from spf.mr.lambda_.logic_language_services import LogicLanguageServices
      type_repository_ = LogicLanguageServices.get_type_repository()

    split = string_.split(Term.TYPE_SEPARATOR)
    if len(split) != 2:
      raise LogicalExpressionRuntimeError('Constant syntax error: %s' % string_)
    type_ = type_repository_.get_type(split[1])
    if type_ is None:
      type_ = type_repository_.get_type_create_if_needed(split[1])
    if type_ is None:
      raise LogicalExpressionRuntimeError('Unknown type for: %s' % string_)
    return LogicalConstant.create(string_, type_)

  class Reader(object):
    @staticmethod
    def is_valid(string_):
      return LogicalConstantBuilder.is_valid_name(string_)

    @staticmethod
    def read(string_, mapping, type_repository, type_comparator, reader):
      return LogicalConstantBuilder.read(string_, type_repository)


class WrappedConstant(object):
  def __init__(self_, constant_):
    self_.constant_ = constant_

  def __eq__(self_, other):
    return isinstance(other, WrappedConstant) and self_.constant_.do_equals(other.constant_)

  def calculate_hash_code(self_):
    return self_.constant_.calculate_hash_code()
