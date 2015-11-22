#!/usr/bin/env python
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.lambda_ import Lambda


class ReplaceBoundVariables(LogicalExpressionVisitorI):
    def __init__(self):
        self.variable_mapping = {}
        self.result = None

    def of(self, expr):
        visitor = ReplaceBoundVariables()
        visitor.visit(expr)
        return visitor.result

    def visit_lambda(self, lambda_):
        new_var = Variable(lambda_.get_argument().get_type())
        self.variable_mapping.update({lambda_.get_argument(): new_var})
        lambda_.get_body().accept(self)
        self.variable_mapping.pop(lambda_.get_argument(), None)
        self.result = Lambda(new_var, self.result)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        new_predicate = self.result
        new_arguments = []
        arg_changed = False
        for arg in literal.get_arguments():
            arg.accept(self)
            new_arguments.append(self.result)
            if arg != self.result:
                arg_changed = True

        if arg_changed:
            self.result = Literal(new_predicate, new_arguments)
        else:
            if new_predicate == literal.get_predicate():
                self.result = literal
            else:
                self.result = Literal(new_predicate, literal.get_arguments())

    def visit_logical_constant(self, logical_constant):
        self.result = logical_constant

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        if variable in self.variable_mapping:
            self.result = self.variable_mapping.get(variable)
        else:
            self.result = variable
