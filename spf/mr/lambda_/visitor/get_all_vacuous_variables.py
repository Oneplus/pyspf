#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetAllVacuousVariables(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.vacuous_variables_ = set()

  @staticmethod
  def of(expr_):
    visitor = GetAllVacuousVariables()
    visitor.visit(expr_)
    return visitor.vacuous_variables_

  def visit_lambda(self_, lambda_):
    self_.vacuous_variables_.add(lambda_.get_argument())
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
    self_.vacuous_variables_.remove(variable_)
