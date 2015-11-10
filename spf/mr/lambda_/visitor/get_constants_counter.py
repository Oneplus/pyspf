#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class GetConstantsCounter(AbstractLogicalExpressionVisitor):
    def __init__(self):
        self.constants = {}

    @staticmethod
    def of(expr):
        visitor = GetConstantsCounter()
        visitor.visit(expr)
        return visitor.constants

    def visit_lambda(self, lambda_):
        lambda_.get_argument().accept(self)
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        if logical_constant not in self.constants:
            self.constants[logical_constant] = 0
        self.constants[logical_constant] += 1

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
