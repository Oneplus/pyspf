#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetConstantsSet(LogicalExpressionVisitorI):
    def __init__(self):
        self.constants = set()

    @staticmethod
    def of(expr):
        visitor = GetConstantsSet()
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
        self.constants.add(logical_constant)

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
