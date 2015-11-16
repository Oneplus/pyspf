#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetAllStrings(LogicalExpressionVisitorI):
    def __init__(self):
        self.constant_strings = []

    @staticmethod
    def of(expr):
        visitor = GetAllStrings()
        visitor.visit(expr)
        return visitor.constant_strings

    def visit_lambda(self, lambda_):
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        self.constant_strings.append(logical_constant.get_name())

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
