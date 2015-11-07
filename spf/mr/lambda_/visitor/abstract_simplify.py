#!/usr/bin/env python

from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.visitor.is_constaining_variable import IsContainingVariable
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor
from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType

class AbstractSimplify(AbstractLogicalExpressionVisitor):
  def __init__(self_, strip_lambdas_):
    self_.strip_lambda_ = strip_lambdas_
    self_.temp_return_ = None

  def strip_redundant_lambda(self_, lambda_arg_, lambda_body_):
    '''
    Handle the cases where the lambda operator is redundant. For example 
    (lambda $0:e (foo:<e,<e,t>> bar:e $0)) should be (foo:<e,<e,t>> bar:e)
    '''
    if not isinstance(lambda_body_, Literal):
      return None
    literal_ = lambda_body_
    args_ = literal_.get_arguments()
    if (not isinstance(literal_.get_predicate_type(), RecursiveComplexType) and
        args[-1] == lambda_arg_):
      # At such condition, the lambda operator is redundant. Also, we need to
      # verify that the variable is not used in any other place in the expression
      used_else_where = IsContainingVariable.of(literal_.get_predicate(), lambda_arg_)
      if not used_else_where:
        for arg_ in args_:
          if IsContainingVariable.of(arg_, lambda_arg_):
            used_else_where = True
            break

      if used_else_where:
        return None
      elif len(args_) == 1:
        return literal_.get_predicate()
      else:
        return Literal(literal_.get_predicate(), args_[0: -1])
    else:
      return None

  def visit_lambda(self_, lambda_):
    '''
    Parameter
    ---------
    lambda_: spf.mr.lambda_.lambda_.Lambda
      The input lambda expression
    '''
    lambda_.get_argument().accept(self_)
    if self_.temp_return_ is None:
      return
    new_arg_ = self_.temp_return_

    lambda_.get_body().accept(self_)
    if self_.temp_return_ is None:
      return
    new_body_ = self_.temp_return_

    if (self_.strip_lambda_ and isinstance(new_arg_, Variable)):
      lambda_stripped_ = self_.strip_redundant_lambda(new_arg_, new_body_)
      if lambda_stripped_ is not None:
        self_.temp_return_ = lambda_stripped_
        return

    if new_body_ == lambda_.get_body() and new_arg_ == lambda_.get_argument():
      self_.temp_return_ = lambda_
    else:
      if isinstance(new_arg_, Variable):
        self_.temp_return_ = None

  def visit_literal(self_, literal_):
    '''
    Basiclly, it seems erase all the last parameter

    Parameter
    ---------
    literal_: spf.mr.lambda_.literal.Literal
      The input literal
    '''
    literal_.get_predicate().accept(self_)
    simplified_predicate_ = self_.temp_return_

    new_args_ = []
    args_changed = False
    for arg_ in literal_.get_arguments():
      arg_.accept(self_)
      if self_.temp_return_ != arg_:
        args_changed = True
      new_args_.append(self_.temp_return_)

    if args_changed:
      simplified_args = new_args_
    else:
      simplified_args = literal_.get_arguments()

    new_predicate_ = simplified_predicate_

    if self_.should_consume_args(new_predicate_):
      change_due_to_lambda_application = False
      for arg_ in simplified_args:
        if not self_.should_consume_args(new_predicate):
          break
      

  def visit_logical_constant(self_, logical_constant_):
    self_.temp_return_ = logical_constant_

  def visit_logical_expression(self_, logical_expr_):
    logical_expr_.accept(self_)

  def should_consume_args(self_, new_predicate_):
    return (new_predicate_.get_type().is_complex() and
        not isinstance(new_predicate_, LogicalConstant) and
        not isinstance(new_predicate_, Variable))
