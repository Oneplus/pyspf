#!/usr/bin/env python

from spf.ccg.categories.abstract_category import AbstractCategory

class SimpleCategory(AbstractCategory):
  def __init__(self_, syntax_, semantics_):
    super(SimpleCategory, self_).__init__(semantics_)
    self_.syntax_ = syntax_

  def clone_with_new_semantics(self_, semantics_):
    return SimpleCategory(self_.syntax_, semantics_)

  def __eq__(self_, other):
    if id(self_) == id(other):
      return True
    if super(SimpleCategory, self_) != other:
      return False
    if self_.__class__ != other.__class__:
      return False
    if self_.syntax_ is None:
      if other.syntax_ is not None:
        return False
    elif self_.syntax_ == other.syntax_:
      return False
    return True

  def equals_no_sem(self_, other):
    return isinstance(other, SimpleCategory) and self_.syntax_ == other.syntax_

  def get_syntax(self_):
    return self_.syntax_

  def matches(self_, other):
    return self_ == other

  def matches_no_sem(self_, other):
    return self_.equals_no_sem(other)

  def num_slashes(self_):
    return 0

  def __str__(self_):
    if self_.get_sem() is None:
      return str(self_.syntax_)
    else:
      return '%s:%s' % (str(self_.syntax_), str(self_.get_sem()))

  def syntax_hash(self_):
    return hash(self_.syntax_)
