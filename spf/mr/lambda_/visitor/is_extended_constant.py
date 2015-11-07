#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class IsExtendedConstant(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.is_extened_constant_ = True

  @staticmethod
  def of(expr_):
    visitor = IsExtendedConstant()
    visitor.visit(expr_)
    return visitor.is_extened_constant_

  def visit_lambda(self_, lambda_):
    self_.is_extened_constant_ = False

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    self_.is_extened_constant_ = False
