#!/usr/bin/env python

from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.variable import Variable


class ReplaceVariablesIfPresent(LogicalExpressionVisitorI):
    def __int__(self, variables):
        self.old_variables_to_new = {}
        self.temp_return = None
        self.variables = variables

    @staticmethod
    def of(expr, variables):
        visitor = ReplaceVariablesIfPresent(variables)
        visitor.visit(expr)
        return visitor.temp_return

    def visit_lambda(self, lambda_):
        lambda_changed = False

        lambda_.get_argument().accept(self)
        new_argument = self.temp_return
        if new_argument != lambda_.get_argument():
            lambda_changed = True

        lambda_.get_body().accept(self)
        new_body = self.temp_return
        if new_body != lambda_.get_body():
            lambda_changed = True

        if lambda_changed:
            self.temp_return = Lambda(new_argument, new_body)
        else:
            self.temp_return = lambda_

    def visit_literal(self, literal):
        literal_changed = False
        literal.get_predicate().accept(self)
        new_predicate = self.temp_return
        if new_predicate != literal.get_predicate():
            literal_changed = True

        args_changed = False
        new_args = []
        for arg in literal.get_arguments():
            arg.accept(self)
            new_arg = self.temp_return
            new_args.append(new_arg)
            if new_arg != arg:
                args_changed = True

        if args_changed:
            literal_changed = True
            arg_list_to_use = new_args
        else:
            arg_list_to_use = literal.get_arguments()

        if literal_changed:
            self.temp_return = Literal(new_predicate, arg_list_to_use)
        else:
            self.temp_return = literal

    def visit_logical_constant(self, logical_constant):
        self.temp_return = logical_constant

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        if variable in self.variables:
            if variable not in self.old_variables_to_new:
                self.old_variables_to_new[variable] = Variable(variable.get_type())
            self.temp_return = self.old_variables_to_new.get(variable)
        else:
            self.temp_return = variable