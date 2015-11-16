#!/usr/bin/env python
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.visitor.is_containing_variable import IsContainingVariable
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI
from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType


class SimplifyI(LogicalExpressionVisitorI):
    def __init__(self, strip_lambdas):
        self.strip_lambda = strip_lambdas
        self.temp_return = None

    @staticmethod
    def strip_redundant_lambda(lambda_arg, lambda_body):
        """
        Handle the cases where the lambda operator is redundant. e.g.

         `(lambda $0:e (foo:<e,<e,t>> bar:e $0)) should be (foo:<e,<e,t>> bar:e)`

        :param lambda_arg:
        :param lambda_body:
        :return:
        """
        if not isinstance(lambda_body, Literal):
            return None

        literal = lambda_body
        args = literal.get_arguments()
        if (not isinstance(literal.get_predicate_type(), RecursiveComplexType) and
                    args[-1] == lambda_arg):
            # At such condition, the lambda operator is redundant. Also, we need to
            # verify that the variable is not used in any other place in the expression
            used_else_where = IsContainingVariable.of(literal.get_predicate(), lambda_arg)
            if not used_else_where:
                for arg in args:
                    if IsContainingVariable.of(arg, lambda_arg):
                        used_else_where = True
                        break

            if used_else_where:
                return None
            elif len(args) == 1:
                return literal.get_predicate()
            else:
                return Literal(literal.get_predicate(), args[0: -1])
        else:
            return None

    def visit_lambda(self, lambda_):
        """

        :param lambda_: spf.mr.lambda_.lambda_.Lambda, The input lambda expression
        :return:
        """
        lambda_.get_argument().accept(self)
        if self.temp_return is None:
            return
        new_arg = self.temp_return

        lambda_.get_body().accept(self)
        if self.temp_return is None:
            return
        new_body = self.temp_return

        if self.strip_lambda and isinstance(new_arg, Variable):
            lambda_stripped = self.strip_redundant_lambda(new_arg, new_body)
            if lambda_stripped is not None:
                self.temp_return = lambda_stripped
                return

        if new_body == lambda_.get_body() and new_arg == lambda_.get_argument():
            self.temp_return = lambda_
        else:
            if isinstance(new_arg, Variable):
                self.temp_return = Lambda(new_arg, new_body)
            else:
                self.temp_return = None

    def visit_logical_constant(self, logical_constant):
        self.temp_return = logical_constant

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)
