#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class IsValid(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.bound_variables_ = set()
    self_.result_ = True

  @staticmethod
  def of(expr_):
    visitor = IsValid()
    visitor.visit(expr_)
    return visitor.constant_strings_

  def visit_lambda(self_, lambda_):
    if self_.bound_variables_.add(lambda_.get_argument()):
      self_.result_ = False
    lambda_.get_argument().accept(self_)
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
