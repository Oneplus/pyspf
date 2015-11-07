#!/usr/bin/env python

from spf.mr.lambda_.visitor.abstract_simplify import AbstractSimplify

class Simplify(AbstractSimplify):
  def __init__(self_, strip_lambdas_):
    super(Simplify, self_).__init__(strip_lambdas_)

  def of(expr_, strip_lambdas_=False):
    visitor = Simplify(strip_lambdas_)
    visitor.visit(expr_)
    return visitor.temp_return_

  def visit_variable(self_, variable_):
    self_.temp_return_ = variable_
