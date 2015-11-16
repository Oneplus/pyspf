#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class IsExtendedConstant(LogicalExpressionVisitorI):
    def __init__(self):
        self.is_extened_constant = True

    @staticmethod
    def of(expr):
        visitor = IsExtendedConstant()
        visitor.visit(expr)
        return visitor.is_extened_constant

    def visit_lambda(self, lambda_):
        self.is_extened_constant = False

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.is_extened_constant = False
