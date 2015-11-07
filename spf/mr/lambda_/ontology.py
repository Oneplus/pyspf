#!/usr/bin/env python

from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.mr.lambda_.logical_const import LogicalConstant, WrappedConstant

class Ontology(object):
  def __init__(self_, constants_, is_closed_):
    self_.is_closed_ = is_closed_
    self_.constants_ = {}
    self_.constants_by_name = {}

    for constant_ in constants_:
      # TODO
      self_.constants_({constant_, constants_})
      self_.constants_by_name.update({constants_.get_name(), constants_})

  def add(self_, constant_, force):
    if constant_ not in self_.constants_:
      if (force or not self_.is_closed):
        constants_.update({constant_, constant_})
        constants_by_name.update({constant_.get_name(), constant_})
      else:
        raise LogicalExpressionRuntimeError(
            'Closed ontolog. Failed to add %s' % str(constant_))
    return self_.get(constant_.get_name())

  def get(self_, constant_):
    if isinstance(constant_, LogicalConstant):
      return self_.constants_.get(constant_, None)
    elif isinstance(constant_, str):
      return self_.constants_by_name.get(constant_, None)
    else:
      raise LogicalExpressionRuntimeError('Not known type of input argument.')

  def contains(self_, constant_):
    if isinstance(constant_, LogicalConstant):
      return constant_ in self_.constants_
    elif isinstance(constant_, str):
      return constant_ in self_.constants_by_name
    else:
      raise LogicalExpressionRuntimeError('Not known type of input argument.')

  def get_all_constants(self_):
    return self_.constants_.values()

  def get_all_predicates(self_):
    predicates = set()
    for key, value in self_.constants_.iteritems():
      if value.get_type().is_complex():
        predicates.add(value)
    return predicates

  def get_or_add(self_, constant_, force):
    if self_.contains(constant_):
      return self_.get(constant_)
    else:
      return self_.add(constant_, force)

  def is_closed(self_):
    return self_.is_closed_

