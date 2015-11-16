#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetAllSimpleConstantNames(LogicalExpressionVisitorI):
    def __init__(self):
        self.names = {}

    @staticmethod
    def of(expr):
        visitor = GetAllSimpleConstantNames()
        visitor.visit(expr)
        return visitor.names

    def visit_lambda(self, lambda_):
        lambda_.get_argument().accept(self)
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        if not logical_constant.get_type().is_complex():
            name = logical_constant.get_name()
            if name not in self.names:
                self.names[name] = 0
            self.names[name] += 1

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
