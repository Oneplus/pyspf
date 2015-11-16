#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetAllVacuousVariables(LogicalExpressionVisitorI):
    """ Vacuous variables is like (lambda $0:e (predicate:<e,t> UK)) """
    def __init__(self):
        self.vacuous_variables = set()

    @staticmethod
    def of(expr):
        visitor = GetAllVacuousVariables()
        visitor.visit(expr)
        return visitor.vacuous_variables

    def visit_lambda(self, lambda_):
        self.vacuous_variables.add(lambda_.get_argument())
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
        self.vacuous_variables.remove(variable)
