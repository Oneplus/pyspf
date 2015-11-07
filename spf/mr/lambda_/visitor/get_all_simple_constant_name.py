#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetAllSimpleConstantNames(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.names_ = {}

  @staticmethod
  def of(expr_):
    visitor = GetAllSimpleConstantNames()
    visitor.visit(expr_)
    return visitor.names_

  def visit_lambda(self_, lambda_):
    lambda_.get_argument().accept(self_)
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    if not logical_constant_.get_type().is_complex():
      if logical_constant_.get_name() is not in self_.names_:
        self_.names_[logical_constant_.get_name()] = 0
      self_.names_[logical_constant_.get_name()] += 1

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
