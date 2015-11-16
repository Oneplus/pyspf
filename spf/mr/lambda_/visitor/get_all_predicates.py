#!/usr/bin/env python

from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class GetAllPredicates(LogicalExpressionVisitorI):
    def __init__(self):
        self.predicates = set()

    @staticmethod
    def of(expr):
        visitor = GetAllPredicates()
        visitor.visit(expr)
        return visitor.predicates

    def visit_lambda(self, lambda_):
        lambda_.get_argument().accept(self)
        lambda_.get_body().accept(self)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            arg.accept(self)

    def visit_logical_constant(self, logical_constant):
        if (isinstance(logical_constant.get_type(), ComplexType) and
                not LogicLanguageServices.is_coordination_predicate(logical_constant) and
                not LogicLanguageServices.is_array_index_predicate(logical_constant) and
                not LogicLanguageServices.is_array_sub_predicate(logical_constant)):
            self.predicates.add(logical_constant)

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return
