#!/usr/bin/env python

from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.mr.lambda_.variable import Variable
from spf.utils.lisp_reader import LispReader
import logging

class Lambda(LogicalExpression):
  HEAD_STRING = 'lambda'
  PREFIX = LogicalExpression.PARENTHESIS_OPEN + HEAD_STRING # (lambda
  LOG = logging.getLogger(__name__)

  def __init__(self_, argument_, body_, type_repository=None):
    super(Lambda, self_).__init__()
    if type_repository is None:
      type_repository = LogicLanguageServices.get_type_repository()

    self_.argument_ = argument_
    self_.body_ = body_
    self_.type_ = type_repository.get_type_create_if_needed(
        self_.body_.get_type(),
        self_.argument_.get_type())

  def accept(self_, visitor):
    visitor.visit(self_)


  def calculate_hash_code(self_):
    ret = 31 + (0 if self_.argument_ is None else self_.argument_.calculate_hash_code())
    ret = 31 * ret + (0 if self_.body_ is None else self_.body_.calculate_hash_code())
    ret = 31 * ret + (0 if self_.type_ is None else self_.type_.calculate_hash_code())
    return ret

  def get_argument(self_):
    return self_.argument_

  def get_body(self_):
    return self_.body_

  def get_complex_type(self_):
    return self_.type_

  def get_type(self_):
    return self_.type_

  def do_equals(self_, other, mapping):
    if id(self_) == id(other):
      return True
    if not isinstance(other, Lambda):
      return False
    if self_.type_ is None:
      if other.type_ is not None:
        return False
    elif self_.type_ == other.type_:
      return False

    if self_.argument_ is None:
      if other.argument_ is not None:
        return False
    elif self_.argument_ is not None:
      mapping.update({self_.argument_: other.argument_})

    ret = True
    if self_.body_ is None:
      if other.body_ is not None:
        ret = False
    else:
      ret = self_.body_.equals(other.body_, mapping)

    mapping.pop(self_.argument_, None)
    return ret

  class Reader(object):
    @staticmethod
    def is_valid(string_):
        return string_.startswith(Lambda.PREFIX)

    @staticmethod
    def read(string_, mapping, type_repository, type_comparator, reader):
      lisp_reader = LispReader(string_)
      lisp_reader.next()

      variables_org_size = len(mapping)
      variable = reader.read(lisp_reader.next(), mapping,
          type_repository, type_comparator)

      if not isinstance(variable, Variable):
        raise LogicalExpressionRuntimeError('Invalid lambda argument: ' + string_)
      if variables_org_size + 1 != len(mapping):
        raise LogicalExpressionRuntimeError(
            'Lambda expression must introduce a new variable: ' + string_)

      body = reader.read(lisp_reader.next(), mapping, type_repository, type_comparator)

      if lisp_reader.has_next():
        raise LogicalExpressionRuntimeError('Invalid lambda expression: ' + string_)

      removed = None
      for key, var in mapping.iteritems():
        if var == variable:
          removed = key
          break
      if removed is None:
        raise LogicalExpressionRuntimeError(
            'Failed to remove variable from mapping. Something werid is happening')

      mapping.pop(removed, None)
      return Lambda(variable, body)
