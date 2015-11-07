#!/usr/bin/env python

from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor

class GetStructure(AbstractLogicalExpressionVisitor):
  ''' This visitor remove the lexical items in lambda calculus, like
  (lambda $0 (foo:<e,<e,t>> $0 bar) to (lambda $0 (ann:<e,<e,t>> $0 ann))
  '''
  DEFAULT_ANONNYMOUS_TAG = 'anno'

  def __init__(self_, anonnymous_name):
    self_.anonnymous_name_ = anonnymous_name_
    self_.temp_return_ = None

  @staticmethod
  def of(expr_, anonnymous_name_=DEFAULT_ANONNYMOUS_TAG):
    visitor = GetStructure(anonnymous_name_)
    visitor.visit(expr_)
    return visitor.temp_return_

  def visit_lambda(self_, lambda_):
    lambda_.get_body().accept(self_)
    if lambda_.get_body() == self_.temp_return_:
      self_.temp_return_ = lambda_
    else:
      self_.temp_return_ = Lambda(lambda_.get_argument(), self_.temp_return_)

  def visit_literal(self_, literal_):
    literal_.get_predicate().accept(self_)
    new_predicate_ = self_.temp_return_

    args_changed_ = False
    new_args_ = []

    for arg_ in literal_.get_arguments():
      arg_.accept(self_)
      new_args_.append(self_.temp_return_)
      if arg_ != self.temp_return_:
          args_changed_ = True

    if args_changed_ or new_predicate_ != literal_.get_predicate():
      self_.temp_return_ = Literal(new_predicate_,
          new_args_ if args_changed_ else literal_.get_arguments())
    else:
      self_.temp_return_ = literal_

  def visit_logical_constant(self_, logical_constant_):
    self_.temp_return_ = LogicalConstant.create(
        LogicalConstant.make_name(self_.anonnymous_name_, logical_constant_.get_type()),
        logical_constant_.get_type())

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def visit_variable(self_, variable_):
    self_.temp_return_ = variable_
