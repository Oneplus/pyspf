#!/usr/bin/env python

from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class GetHeadString(AbstractLogicalExpressionVisitor):
    VARIABLE_HEAD_STRING = 'var'

    def __init__(self):
        self.head_string = None

    @staticmethod
    def of(expr):
        visitor = GetHeadString()
        visitor.visit(expr)
        return visitor.head_string

    def visit_lambda(self, lambda_):
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)

    def visit_logical_constant(self, logical_constant):
        self.head_string = logical_constant.get_name()

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.head_string = GetHeadString.VARIABLE_HEAD_STRING
