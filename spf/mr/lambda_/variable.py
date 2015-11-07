#!/usr/bin/env python

from spf.mr.lambda_.term import Term
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
import logging

class Variable(Term):
  LOG = logging.getLogger(__name__)
  PREFIX = '$'

  def __init__(self_, type_):
    super(Variable, self_).__init__(type_)

  def accept(self_, visitor):
    visitor.visit(self_)

  def __eq__(self_, other):
    return self_ == other

  def do_equals(self_, other, mapping):
    if self_ in mapping:
      return mapping[self_] == other
    elif self_ not in mapping and other not in mapping.values():
      return other == self_
    else:
      return False

  class Reader(object):
    @staticmethod
    def is_valid(string_):
      return string_.startswith(Variable.PREFIX)

    @staticmethod
    def read(string_, mapping, type_repository, type_comparator, reader):
      ''' Read variable from string like, $0:e '''
      split = string_.split(Term.TYPE_SEPARATOR)
      if len(split) == 2:
        type_ = type_repository.get_type_create_if_needed(split[1])
        if type_ is None:
          raise LogicalExpressionRuntimeError('Invalid Type')
        if split[0] in mapping:
          raise LogicalExpressionRuntimeError(
              'Variable overwrite is not supported, please supply unique names')
        variable_ = Variable(type_)
        mapping[split[0]] = variable_
        return variable_
      else:
        if string_ in mapping:
          return mapping.get(string_, None)
        else:
          raise LogicalExpressionRuntimeError('Undefined variable reference: %s' % string_)
