#!/usr/bin/env python

from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.visitor.logical_expr_visitor import AbstractLogicalExpressionVisitor


class GetStructure(AbstractLogicalExpressionVisitor):
    """
    This visitor remove the lexical items in lambda calculus, e.g.
    (lambda $0 (foo:<e,<e,t>> $0 bar) --> (lambda $0 (ann:<e,<e,t>> $0 ann))
    """
    DEFAULT_ANONYMOUS_TAG = 'anno'

    def __init__(self, anonymous_name):
        self.anonymous_name = anonymous_name
        self.temp_return = None

    @staticmethod
    def of(expr, anonymous_name=DEFAULT_ANONYMOUS_TAG):
        visitor = GetStructure(anonymous_name)
        visitor.visit(expr)
        return visitor.temp_return

    def visit_lambda(self, lambda_):
        lambda_.get_body().accept(self)
        if lambda_.get_body() == self.temp_return:
            self.temp_return = lambda_
        else:
            self.temp_return = Lambda(lambda_.get_argument(), self.temp_return)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        new_predicate = self.temp_return

        args_changed = False
        new_args = []

        for arg in literal.get_arguments():
            arg.accept(self)
            new_args.append(self.temp_return)
            if arg != self.temp_return:
                args_changed = True

        if args_changed or new_predicate != literal.get_predicate():
            self.temp_return = Literal(new_predicate, new_args if args_changed else literal.get_arguments())
        else:
            self.temp_return = literal

    def visit_logical_constant(self, logical_constant):
        self.temp_return = LogicalConstant.create(
            LogicalConstant.make_name(self.anonymous_name, logical_constant.get_type()),
            logical_constant.get_type())

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.temp_return = variable
