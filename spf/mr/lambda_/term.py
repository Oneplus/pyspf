#!/usr/bin/env python

from spf.mr.lambda_.logical_expr import LogicalExpression

class Term(LogicalExpression):
  TYPE_SEPARATOR = ':'

  def __init__(self_, type_):
    super(Term, self_).__init__()
    self_.type_ = type_

  def calculate_hash_code(self_):
    return 31 * 1 + (0 if self_.type_ is None else hash(self_.type_))

  def __eq__(self_, other):
    return (isinstance(other, Term) and
        hash(other) == hash(self_) and
        self_.do_equals(other))

  def get_type(self_):
    return self_.type_

  def do_equals(self_, other, mapping):
    if self_ is None:
      return True
    if other is None:
      return False
    if type(self_) != type(other):
      return False
    if self_.type_ is None:
      if other.type_ is not None:
        return False
    elif self_.type_ != other.type_:
      return False
    return True
