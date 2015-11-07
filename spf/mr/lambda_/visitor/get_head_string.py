#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetHeadString(AbstractLogicalExpressionVisitor):
  VARIABLE_HEAD_STRING = 'var'

  def __init__(self_):
    self_.head_string_ = None

  @staticmethod
  def of(expr_):
    visitor = GetHeadString()
    visitor.visit(expr_)
    return visitor.head_string_

  def visit_lambda(self_, lambda_):
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    self_.head_string_ = logical_constant_.get_name()

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    self_.head_string_ = GetHeadString.VARIABLE_HEAD_STRING
