#!/usr/bin/env python
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.variable import Variable
#from spf.mr.lambda_.visitor.is_containing_variable import IsContainingVariable
#from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType


class LogicalExpressionVisitorI(object):
    def visit(self, expr):
        if isinstance(expr, Lambda):
            return self.visit_lambda(expr)
        elif isinstance(expr, Literal):
            return self.visit_literal(expr)
        elif isinstance(expr, LogicalConstant):
            return self.visit_logical_constant(expr)
        elif isinstance(expr, Variable):
            return self.visit_variable(expr)
        elif isinstance(expr, LogicalExpression):
            return self.visit_logical_expression(expr)
        else:
            raise RuntimeError('Illegal Type!')

    def visit_lambda(self, lambda_):
        """

        :param lambda_:
        :type lambda_: Lambda
        :return:
        """
        raise NotImplementedError()

    def visit_literal(self, literal):
        """

        :param literal:
        :type literal: Literal
        :return:
        """
        raise NotImplementedError()

    def visit_logical_constant(self, logical_constant):
        """

        :param logical_constant:
        :type logical_constant: LogicalConstant
        :return:
        """
        raise NotImplementedError()

    def visit_logical_expression(self, logical_expr):
        """

        :param logical_expr:
        :type logical_expr: LogicalExpression
        :return:
        """
        raise NotImplementedError()

    def visit_variable(self, variable):
        """

        :param variable:
        :type variable: Variable
        :return:
        """
        raise NotImplementedError()
