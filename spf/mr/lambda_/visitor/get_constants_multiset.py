#!/usr/bin/env python

from collections import Counter
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetConstantsMultiSet(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.constants_ = Counter()

  @staticmethod
  def of(expr_):
    visitor = GetConstantsMultiSet()
    visitor.visit(expr_)
    return visitor.constants_

  def visit_lambda(self_, lambda_):
    lambda_.get_argument().accept(self_)
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    self_.constants_.update([logical_constant_])

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
