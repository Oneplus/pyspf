#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetParameterVariablesList(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.param_list_ = []

  @staticmethod
  def of(expr_):
    visitor = GetParameterVariablesList()
    visitor.visit(expr_)
    return visitor.param_list_

  def visit_lambda(self_, lambda_):
    self_.param_list_.append(lambda_.get_argument())
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
