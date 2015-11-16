#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetParameterVariablesList(LogicalExpressionVisitorI):
    def __init__(self):
        self.param_list = []

    @staticmethod
    def of(expr):
        visitor = GetParameterVariablesList()
        visitor.visit(expr)
        return visitor.param_list

    def visit_lambda(self, lambda_):
        self.param_list.append(lambda_.get_argument())
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
