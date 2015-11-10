#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class GetAllSimpleLogicalConstants(AbstractLogicalExpressionVisitor):
    def __init__(self):
        self.constants = set()

    @staticmethod
    def of(expr):
        visitor = GetAllSimpleLogicalConstants()
        visitor.visit(expr)
        return visitor.constants

    def visit_lambda(self, lambda_):
        lambda_.get_argument().accept(self)
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        type_ = logical_constant.get_type()
        if not type_.is_array() and not type_.is_complex():
            self.constants.add(logical_constant)

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
