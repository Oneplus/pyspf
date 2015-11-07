#!/usr/bin/env python

from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logical_expr import LogicalExpression

class AbstractLogicalExpressionVisitor(object):
  def visit(self_, expr):
    if isinstance(expr, Lambda):
      return self_.visit_lambda(expr)
    elif isinstance(expr, Literal):
      return self_.visit_literal(expr)
    elif isinstance(expr, LogicalConstant):
      return self_.visit_logical_constant(expr)
    elif isinstance(expr, Variable):
      return self_.visit_variable(expr)
    elif isinstance(expr, LogicalExpression):
      return self_.visit_logical_expression(expr)
    else:
      raise RuntimeError('Illegal Type!')

  def visit_lambda(self_, lambda_):
    raise NotImplementedError()

  def visit_literal(self_, literal_):
    raise NotImplementedError()

  def visit_logical_constant(self_, logical_constant_):
    raise NotImplementedError()

  def visit_logical_expression(self_, logical_expr_):
    raise NotImplementedError()

  def visit_variable(self_, variable):
    raise NotImplementedError()
