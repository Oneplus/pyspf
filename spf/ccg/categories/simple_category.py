#!/usr/bin/env python

from spf.ccg.categories.abstract_category import AbstractCategory


class SimpleCategory(AbstractCategory):
    def __init__(self, syntax, semantics_):
        super(SimpleCategory, self).__init__(semantics_)
        self.syntax = syntax

    def clone_with_new_semantics(self, semantics):
        return SimpleCategory(self.syntax, semantics)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if super(SimpleCategory, self) != other:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.syntax is None:
            if other.syntax_ is not None:
                return False
        elif self.syntax == other.syntax_:
            return False
        return True

    def equals_no_sem(self, other):
        return isinstance(other, SimpleCategory) and self.syntax == other.syntax

    def get_syntax(self):
        return self.syntax

    def matches(self, other):
        return self == other

    def matches_no_sem(self, other):
        return self.equals_no_sem(other)

    def num_slashes(self):
        return 0

    def __str__(self):
        if self.get_sem() is None:
            return str(self.syntax)
        else:
            return '%s:%s' % (str(self.syntax), str(self.get_sem()))

    def syntax_hash(self):
        return hash(self.syntax)
