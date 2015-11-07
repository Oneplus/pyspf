#!/usr/bin/env python

from spf.mr.lambda_.logical_constant import LogicalConstant
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetPredicateCounts(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.predicates_ = {}

  @staticmethod
  def of(expr_):
    visitor = GetPredicateCounts()
    visitor.visit(expr_)
    return visitor.predicates_

  def visit_lambda(self_, lambda_):
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    if isinstance(literal_.get_predicate(), LogicalConstant):
      if literal_.get_predicate() in self_.predicates_:
        self_.predicates_[literal_.get_predicate()] = 0
      self_.predicates_[literal_.get_predicate()] += 1

    literal_.get_predicate().accept(self_)
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    return

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
