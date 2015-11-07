#!/usr/bin/env python
from spf.ccg.categories.abstract_category import AbstractCategory
from spf.ccg.categories.syntax.slash import Slash

class ComplexCategory(AbstractCategory):
  ''' The complex category '''
  def __init__(self_, syntax_, semantics_):
    super(ComplexCategory, self_).__init__(semantics_)
    self_.syntax_ = syntax_

  def clone_with_new_semantics(self_, semantics_):
    return ComplexCategory(self_.syntax_, semantics_)

  def __eq__(self_, other):
    if not isinstance(other, ComplexCategory):
      return False
    if not self_.equals_no_sem(other):
      return False
    if (self_.get_sem() is not None and other.get_sem() is not None and
        self_.get_sem() != other.get_sem()):
      return False
    return True

  def equals_no_sem(self_, other):
    if not isinstance(other, ComplexCategory):
      return False
    if self_.syntax_ != other.syntax_:
      return False
    return True

  def get_slash(self_):
    return self_.syntax_.get_slash()

  def get_syntax(self_):
    return self_.syntax_

  def has_slash(self_, s):
    return (self_.syntax_.get_slash() == Slash.VERTICAL or
        s == self_.syntax_.get_slash() or
        s == Slash.VERTICAL)

  def matches(self_, other):
    if not isinstance(other, ComplexCategory):
      return False
    if (other.syntax_.get_slash() != self_.syntax_.get_slash() and
        self_.syntax_.get_slash() != Slash.VERTICAL and
        other.syntax_.get_slash() != Slash.VERTICAL):
      return False
    if not self_.matches_no_sem(other):
      return False
    if (self_.get_sem() is not None and
        other.get_sem() is not None and
        not self_.get_sem() == other.get_sem()):
      return False
    return True

  def matches_no_sem(self_, other):
    if not isinstance(other, ComplexCategory):
      return False
    return self_.syntax_ == other.get_syntax()

  def num_slashes(self_):
    return self_.num_slashes()

  def __str__(self_):
    ret = str(self_.syntax_)
    if self_.get_sem() is not None:
      ret += ' : %s' % str(self_.get_sem())
    return ret

  def syntax_hash(self_):
    return hash(self_.syntax_)
