#!/usr/bin/env python

from spf.mr.language.type_.type_ import Type


class ArrayType(Type):
    ARRAY_SUFFIX = '[]'

    def __init__(self, name_, base_type, parent):
        super(ArrayType, self).__init__(name_)
        self.base_type = base_type
        self.parent = parent

    def get_base_type(self):
        return self.base_type

    def get_domain(self):
        return None

    def get_range(self):
        return self

    def is_array(self):
        return True

    def is_complex(self):
        return self.base_type.is_complex()

    def is_extending(self, other):
        if other is None:
            return False

        if self == other:
            return True
        elif other.is_array():
            return self.base_type.is_extending(other.get_base_type())
        else:
            return False if self.parent is None else self.parent.is_extending(self)

    def is_extending_or_extended_by(self, other):
        return other is not None and (self.is_extending(other) or other.is_extending(self))

    def __str__(self):
        return str(self.base_type) + self.ARRAY_SUFFIX
