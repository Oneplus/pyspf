#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class GetVariables(AbstractLogicalExpressionVisitor):
    def __init__(self):
        self.variables = set()

    @staticmethod
    def of(expr):
        visitor = GetVariables()
        visitor.visit(expr)
        return visitor.variables

    def visit_lambda(self, lambda_):
        lambda_.get_argument().accept(self)
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.variables.add(variable)
