#!/usr/bin/env python

from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logical_expr import LogicalExpression


class AbstractLogicalExpressionVisitor(object):
    def visit(self, expr):
        if isinstance(expr, Lambda):
            return self.visit_lambda(expr)
        elif isinstance(expr, Literal):
            return self.visit_literal(expr)
        elif isinstance(expr, LogicalConstant):
            return self.visit_logical_constant(expr)
        elif isinstance(expr, Variable):
            return self.visit_variable(expr)
        elif isinstance(expr, LogicalExpression):
            return self.visit_logical_expression(expr)
        else:
            raise RuntimeError('Illegal Type!')

    def visit_lambda(self, lambda_):
        raise NotImplementedError()

    def visit_literal(self, literal):
        raise NotImplementedError()

    def visit_logical_constant(self, logical_constant):
        raise NotImplementedError()

    def visit_logical_expression(self, logical_expr):
        raise NotImplementedError()

    def visit_variable(self, variable):
        raise NotImplementedError()
