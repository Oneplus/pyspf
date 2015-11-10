#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class IsContainingVariable(AbstractLogicalExpressionVisitor):
    """ Return if the logical expression contains certain variable """

    def __init__(self, var):
        """

        :param var: spf.mr.lambda_.variable.Variable, the targeted variable
        :return:
        """
        self.containing = False
        self.var = var

    @staticmethod
    def of(expr, var):
        visitor = IsContainingVariable(var)
        visitor.visit(expr)
        return visitor.containing

    def visit_lambda(self, lambda_):
        lambda_.get_argument().accept(self)
        if not self.containing:
            lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        if not self.containing:
            for arg in literal.get_arguments():
                arg.accept(self)
                if self.containing: return

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.containing |= (variable == self.var)
