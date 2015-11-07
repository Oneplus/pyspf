#!/usr/bin/env python

class LogicalExpression(object):
  PARENTHESIS_CLOSE = ')'
  PARENTHESIS_OPEN = '('

  def __init__(self_):
    self_.hash_code_cache = -1
    self_.hash_code_calculated = False

  def __hash__(self_):
    if not self_.hash_code_calculated:
      self_.hash_code_cache = self_.calculate_hash_code()
      self_.hash_code_calculated = True
    return self_.hash_code_cache

  def calculate_hash_code(self_):
    raise NotImplementedError

  def __str__(self_):
    raise NotImplementedError

  def do_equals(self_, expr, mapping):
    raise NotImplementedError

  def equals(self_, expr, mapping):
    return (expr is not None and
        expr.hash_code() == self_.hash_code() and
        self_.do_equals(expr, mapping))
