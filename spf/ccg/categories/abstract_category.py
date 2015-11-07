#!/usr/bin/env python

class AbstractCategory(object):
  def __init__(self_, semantics_):
    self_.hash_code_cache_ = None
    self_.hash_code_calculated_ = False
    self_.semantics_ = semantics_

  def __eq__(self_, other):
    if id(self_) == id(other):
      return True
    if other is None:
      return False
    if not isinstance(other, _Category):
      return False
    if self_.semantics_ is None:
      if other.semantics_ is not None:
        return False
    elif self_.semantics_ != other.semantics_:
      return False
    return True

  def clone_with_new_semantics(self_, new_semantics_):
    raise NotImplementedError()

  def equals_no_sem(self_, other):
    raise NotImplementedError()

  def get_sem(self_):
    return self_.semantics_

  def __hash__(self_):
    if not hash_code_calculated_:
      hash_code_cache_ = self_.calculate_hash_code()
      hash_code_calculated_ = True
    return hash_code_cache_

  def matches(self_, c):
    raise NotImplementedError()

  def matches_no_sem(self_, c):
    raise NotImplementedError()

  def num_slashes(self_):
    raise NotImplementedError()

  def calculate_hash_code(self_):
    if self_.semantics_ is None:
      return 0
    return self_.syntax_hash() + hash(self_.semantics_)

  def syntax_hash(self_):
    raise NotImplementedError()
