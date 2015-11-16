#!/usr/bin/env python
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetAllFreeVariables(LogicalExpressionVisitorI):
    """ Free Variables are the unbound variable, e.g. $1 in (lambda $0:e (predicate:<e,<e,t>> $0 $1)) """
    def __init__(self):
        self.bound_variables = set()
        self.free_variables = set()

    @staticmethod
    def of(expr):
        visitor = GetAllFreeVariables()
        visitor.visit(expr)
        return visitor.free_variables

    def visit_lambda(self, lambda_):
        """
        If visiting a lambda expression, collect its variable in the bound_variables
        :param lambda_:
        :return:
        """
        self.bound_variables.add(lambda_.get_argument())
        lambda_.get_body().accept(self)
        self.bound_variables.remove(lambda_.get_argument())

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        if variable not in self.bound_variables:
            self.free_variables.add(variable)
