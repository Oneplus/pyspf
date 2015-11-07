#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetAllStrings(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.constant_strings_ = []

  @staticmethod
  def of(expr_):
    visitor = GetAllStrings()
    visitor.visit(expr_)
    return visitor.constant_strings_

  def visit_lambda(self_, lambda_):
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    self_.constant_strings_.append(logical_constant_.get_name())

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
