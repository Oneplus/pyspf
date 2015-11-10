#!/usr/bin/env python

from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class GetPredicateCounts(AbstractLogicalExpressionVisitor):
    def __init__(self):
        self.predicates = {}

    @staticmethod
    def of(expr):
        visitor = GetPredicateCounts()
        visitor.visit(expr)
        return visitor.predicates

    def visit_lambda(self, lambda_):
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        if isinstance(literal.get_predicate(), LogicalConstant):
            predicate = literal.get_predicate()
            if predicate in self.predicates:
                self.predicates[predicate] = 0
            self.predicates[predicate] += 1

        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
