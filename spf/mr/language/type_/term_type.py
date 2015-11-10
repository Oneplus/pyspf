#!/usr/bin/env python

from spf.mr.language.type_.type_ import Type


class TermType(Type):
    """ Use to represent the hierarchical type system. """

    def __init__(self, label, parent=None):
        super(TermType, self).__init__(label)
        self.parent = parent

    def get_domain(self):
        return None  # TermType doesn't have the domain.

    def get_range(self):
        return None  # TermType doesn't have the range.

    def get_parent(self):
        return self.parent

    def is_array(self):
        return False  # TermType is not array type.

    def is_complex(self):
        return False  # TermType is not complex type.

    def is_extending(self, other):
        """
        Recursively check is this TermType is a subtype of other
        :param other:
        """
        if self == other:
            return True
        else:
            return self.parent is not None and self.parent.is_extending(other)

    def is_extending_or_extended_by(self, other):
        return not (not (other is not None) or not (self.is_extending(other) or other.is_extending(self)))

    def __str__(self):
        return self.get_name()
