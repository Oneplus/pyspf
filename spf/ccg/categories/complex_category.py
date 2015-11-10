#!/usr/bin/env python
# coding=utf-8
from spf.ccg.categories.abstract_category import AbstractCategory
from spf.ccg.categories.syntax.slash import Slash


class ComplexCategory(AbstractCategory):
    """
    The complex category.
    """

    def __init__(self, syntax, semantics):
        super(ComplexCategory, self).__init__(semantics)
        self.syntax = syntax

    def clone_with_new_semantics(self, semantics):
        return ComplexCategory(self.syntax, semantics)

    def __eq__(self, other):
        if not isinstance(other, ComplexCategory):
            return False
        if not self.equals_no_sem(other):
            return False
        if self.get_sem() is not None and other.get_sem() is not None and self.get_sem() != other.get_sem():
            return False
        return True

    def equals_no_sem(self, other):
        if not isinstance(other, ComplexCategory):
            return False
        if self.syntax != other.syntax:
            return False
        return True

    def get_slash(self):
        return self.syntax.get_slash()

    def get_syntax(self):
        return self.syntax

    def has_slash(self, s):
        return (self.syntax.get_slash() == Slash.VERTICAL or
                s == self.syntax.get_slash() or
                s == Slash.VERTICAL)

    def matches(self, other):
        if not isinstance(other, ComplexCategory):
            return False
        if other.syntax.get_slash() != self.syntax.get_slash() \
                and self.syntax.get_slash() != Slash.VERTICAL \
                and other.syntax.get_slash() != Slash.VERTICAL:
            return False
        if not self.matches_no_sem(other):
            return False
        if self.get_sem() is not None and other.get_sem() is not None and self.get_sem() != other.get_sem():
            return False
        return True

    def matches_no_sem(self, other):
        if not isinstance(other, ComplexCategory):
            return False
        return self.get_syntax() == other.get_syntax()

    def num_slashes(self):
        return self.get_syntax().num_slashes()

    def __str__(self):
        ret = str(self.syntax)
        if self.get_sem() is not None:
            ret += ' : %s' % str(self.get_sem())
        return ret

    def syntax_hash(self):
        return hash(self.syntax)
