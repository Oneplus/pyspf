#!/usr/bin/env python

from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor
import logging

class IsTypeConsistent(AbstractLogicalExpressionVisitor):
  ''' Verify typing consistency across the logical form. '''
  LOG = logging.getLogger(__name__)
  def __init__(self_):
    self_.variable_types_ = {}
    self_.well_typed_ = True

  @staticmethod
  def of(expr_):
    visitor = IsTypeConsistent()
    visitor.visit(expr_)
    return visitor.well_typed_

  def visit_lambda(self_, lambda_):
    self_.variable_types_[lambda_.get_argument()] = lambda_.get_argument().get_type()
    lambda_.get_body().accept(self_)
    self_.variable_types_.pop(lambda_.get_argument())

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    literal_typing_ = LogicLanguageServices.compute_literal_typing_for_args(
        literal_.get_predicate_type(),
        literal_.get_arguments())

    if literal_typing_ is None:
      raise RuntimeError('Failed to compute literal typing for. This should never '
          'have happened, typing is computed during creation: %s' % str(literal_))

    for signature_type_, arg_ in zip(literal_typing_[1], literal_.get_arguments()):
      arg_.accept(self_)

      self_.well_typed_ = self_.well_typed_ and self_.verify_literal_arg_typing(
          arg_, signature_type_)

      if not self_.well_typed_:
        LOG.debug('Literal %s is not well-typed. Mismatch between signature type '
            '%s to argument %s.' % (str(literal_), str(signature_type_), str(arg_)))
        return

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return

  def verify_literal_arg_typing(self_, arg_, signature_type_):
    if isinstance(arg, Variable):
      historical_type_ = self_.variable_types_.get(arg_, None)
      if historical_type_ is None:
        self_.variable_types_.update({arg_: arg_.get_type()})
        return arg_.get_type().is_extending_or_extended_by(signature_type_)
      else:
        if signature_type_.is_extending(historical_type_):
          self_.variable_types_.update({arg_: signature_type_})
          return True
        else:
          return historical_type_.is_extending(signature_type_)
    else:
      return (signature_type_.is_array() == arg_.is_array() and
          arg_.get_type().is_extending_or_extended_by(signature_type_))
