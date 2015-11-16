#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class IsValid(LogicalExpressionVisitorI):
    """
    IsValid check if the there is variables that already used in former lambda expression, e.g.:
    (lambda $0:e (lambda $0:e (p:<e,t> $0)))
    """
    def __init__(self):
        self.bound_variables = set()
        self.result = True

    @staticmethod
    def of(expr):
        visitor = IsValid()
        visitor.visit(expr)
        return visitor.result

    def visit_lambda(self, lambda_):
        if lambda_.get_argument() in self.bound_variables:
            self.result = False
        else:
            self.bound_variables.add(lambda_.get_argument())
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
        return
