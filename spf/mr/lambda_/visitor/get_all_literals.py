#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetAllLiterals(AbstractLogicalExpressionVisitor):
  def __init__(self_, arity_):
    self_.arity_ = arity_
    self_.literals_ = []

  @staticmethod
  def of(expr_, arity_=None):
    visitor = GetAllLiterals(arity_)
    visitor.visit(expr_)
    return visitor.literals_

  def visit_lambda(self_, lambda_):
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    if self_.arity_ is None or len(self_.get_arguments()) == self_.arity_:
      self_.literals_.append(literal_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
