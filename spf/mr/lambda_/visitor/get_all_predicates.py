#!/usr/bin/env python

from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetAllPredicates(AbstractLogicalExpressionVisitor):
  def __init__(self_):
    self_.predicates_ = set()

  @staticmethod
  def of(expr_):
    visitor = GetAllPredicates()
    visitor.visit(expr_)
    return visitor.predicates_

  def visit_lambda(self_, lambda_):
    lambda_.get_argument().accept(self_)
    lambda_.get_body().accept(self_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    for arg_ in self_.get_arguments():
      arg_.accept(self_)

  def visit_logical_constant(self_, logical_constant_):
    if (isinstance(logical_constant_.get_type(), ComplexTypeu) and
        not LogicLanguageServices.is_coordination_predicate(logical_constant_) and
        not LogicLanguageServices.is_array_index_predicate(logical_constant_) and
        not LogicLanguageServices.is_array_sub_predicate(logical_constant_)):
      self_.predicates_.add(logical_constant_)

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    return
