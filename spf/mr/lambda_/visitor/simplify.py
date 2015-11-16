#!/usr/bin/env python
from spf.mr.lambda_.visitor.abstract_simplify import SimplifyI


class Simplify(SimplifyI):
    def __init__(self, strip_lambdas):
        super(Simplify, self).__init__(strip_lambdas)

    @staticmethod
    def of(expr, strip_lambdas=False):
        visitor = Simplify(strip_lambdas)
        visitor.visit(expr)
        return visitor.temp_return

    def visit_variable(self, variable):
        self.temp_return = variable
