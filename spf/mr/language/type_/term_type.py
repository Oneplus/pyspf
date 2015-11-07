#!/usr/bin/env python

from spf.mr.language.type_.type_ import Type

class TermType(Type):
  ''' Use to represent the hierarchical type system. '''
  def __init__(self_, label, parent=None):
    super(TermType, self_).__init__(label)
    self_.parent_ = parent

  def get_domain(self_):
    return None # TermType doesn't have the domain.

  def get_range(self_):
    return None # TermType doesn't have the range.

  def get_parent(self_):
    return self_.parent_

  def is_array(self_):
    return False # TermType is not array type.

  def is_complex(self_):
    return False # TermType is not complex type.

  def is_extending(self_, other):
    ''' Recursively check is this TermType is a subtype of other '''
    if self_ == other:
      return True
    else:
      return (self_.parent_ is not None and
          self_.parent_.is_extending(other))

  def is_extending_or_extended_by(self_, other):
    return ((other is not None) and
        (self_.is_extending(other) or other.is_extending(self_)))

  def __str__(self_):
    return self_.get_name()
