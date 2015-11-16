#!/usr/bin/env python
from spf.mr.lambda_.term import Term
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class LogicalExpressionToString(LogicalExpressionVisitorI):
    def __init__(self):
        self.output_string = ""
        self.variable_naming_list = []
        self.defined_variables = set()

    @staticmethod
    def of(expr):
        visitor = LogicalExpressionToString()
        visitor.visit(expr)
        return visitor.output_string

    def visit_lambda(self, lambda_):
        self.output_string += "(lambda "
        lambda_.get_argument().accept(self)
        self.output_string += " "
        lambda_.get_body().accept(self)
        self.output_string += ")"

    def visit_literal(self, literal):
        self.output_string += "("
        literal.get_predicate().accept(self)
        for arg in literal.get_arguments():
            self.output_string += " "
            arg.accept(self)
        self.output_string += ")"

    def visit_logical_constant(self, logical_constant):
        self.output_string += logical_constant.get_name()

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        self.output_string += self.get_variable_name(variable)
        if variable not in self.defined_variables:
            self.output_string += Term.TYPE_SEPARATOR
            self.output_string += variable.get_type().get_name()
            self.defined_variables.add(variable)

    def get_variable_name(self, variable):
        n = 0
        for named_variable in self.variable_naming_list:
            if named_variable == variable:
                return "$%d" % n
            n += 1
        self.variable_naming_list.append(variable)
        return "$%d" % n

    class Printer(object):
        @staticmethod
        def to_string(expr):
            return LogicalExpressionToString.of(expr)
