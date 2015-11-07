#!/usr/bin/env python

from spf.mr.language.type_.type_ import Type

class ArrayType(Type):
  ARRAY_SUFFIX = '[]'

  def __init__(self_, name_, base_type_, parent_):
    super(ArrayType, self_).__init__(name_)
    self_.base_type_ = base_type_
    self_.parent_ = parent_

  def get_base_type(self_):
    return self_.base_type_

  def get_domain(self_):
    return None

  def get_range(self_):
    return self_

  def is_array(self_):
    return True

  def is_complex(self_):
    return self_.base_type_.is_complex()

  def is_extending(self_, other):
    if other is None:
      return False

    if self_ == other:
      return True
    elif other.is_array():
      return self_.base_type_.is_extending(other.get_base_type())
    else:
      return False if self_.parent_ is None else self_.parent_.is_extending(self_)

  def is_extending_or_extended_by(self_, other):
    return other is not None and (self_.is_extending(other) or other.is_extending(self_))

  def __str__(self_):
    return str(self_.base_type_) + ArrayType.ARRAY_SUFFIX
