#!/usr/bin/env python

from spf.ccg.categories.syntax.syntax import AbstractSyntax
from spf.ccg.categories.syntax.slash import Slash

class ComplexSyntax(AbstractSyntax):
  def __init__(self_, left_, right_, slash_):
    self_.left_ = left_
    self_.right_ = right_
    self_.num_slashes_ = left_.num_slashes() + right_.num_slashes() + 1
    self_.slash_ = slash_
    self_.hash_code_ = self_.calculate_hash_code()
    self_.string_ = ComplexSyntax.compute_syntax_string(left_, right_, slash_)

  @staticmethod
  def compute_syntax_string(left_, right_, slash_):
    ret = str(left_) + str(slash_)
    if isinstance(right_, ComplexSyntax):
      ret += '(%s)' % str(right_)
    else:
      ret += str(right_)
    return ret

  def get_left(self_):
    return self_.left_

  def get_right(self_):
    return self_.right_

  def get_slash(self_):
    return self_.slash_

  def num_slashes(self_):
    return self_.num_slashes_

  def calculate_hash_code(self_):
    ret =  31 + (0 if self_.left_ is None else hash(self_.left_))
    ret += 31 * ret + (0 if self.right_ is None else hash(self_.right_))
    ret += 31 * ret + (0 if self.slash_ is None else hash(self_.slash_))
    return ret

  def __hash__(self_):
    return self_.hash_code_

  def __str__(self_):
    return self_.string_
