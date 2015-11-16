#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetAllLiterals(LogicalExpressionVisitorI):
    """
    Get all the literals from the input logical expression. (lambda $0:e (lambda $1:e (predicate:<e,<e,t>> $0 $1))
    """
    def __init__(self, arity):
        """

        :param arity: int, used to specify the arity of the literal
        :return:
        """
        self.arity = arity
        self.literals = []

    @staticmethod
    def of(expr, arity=None):
        visitor = GetAllLiterals(arity)
        visitor.visit(expr)
        return visitor.literals

    def visit_lambda(self, lambda_):
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        if self.arity is None or len(self.get_arguments()) == self.arity:
            self.literals.append(literal)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
