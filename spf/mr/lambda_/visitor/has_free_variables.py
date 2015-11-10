#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class HasFreeVariables(AbstractLogicalExpressionVisitor):
    def __init__(self):
        self.bound_variables = set()
        self.result = False

    @staticmethod
    def of(expr):
        visitor = HasFreeVariables()
        visitor.visit(expr)
        return visitor.result

    def visit_lambda(self, lambda_):
        self.bound_variables.add(lambda_.get_argument())
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)
            if self.result: break

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.result |= (variable not in self.bound_variables)
