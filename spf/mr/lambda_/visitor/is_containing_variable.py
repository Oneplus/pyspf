#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class IsContainingVariable(AbstractLogicalExpressionVisitor):
  ''' Return if the logical expression contains certain variable '''
  def __init__(self_, var_):
    self_.containing_ = False
    self_.var_ = var_

  @staticmethod
  def of(expr_, var_):
    visitor = IsContainingVariable(var_)
    visitor.visit(expr_)
    return visitor.containing_

  def visit_lambda(self_, lambda_):
    lambda_.get_argument().accept(self_)
    if not self_.containing_:
      lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    if not self_.containing_:
      for arg in self_.get_arguments():
        arg.accept(self_)
        if self_.containing_:
          return

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable):
    self_.containing_ |= (variable == self_.var_)
