#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class HasFreeVariables(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.bined_variable_ = set()
    self_.result_ = False

  @staticmethod
  def of(expr_):
    visitor = HasFreeVariables()
    visitor.visit(expr_)
    return visitor.result_

  def visit_lambda(self_, lambda_):
    self_.bined_variable.add(lambda_.get_argument())
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)
      if self_.result_:
        break

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    self_.result_ |= (variable_ not in self_.bined_variable_)
