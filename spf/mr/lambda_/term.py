#!/usr/bin/env python

from spf.mr.lambda_.logical_expr import LogicalExpression


class Term(LogicalExpression):
    TYPE_SEPARATOR = ':'

    def __init__(self, type_):
        super(Term, self).__init__()
        self.type_ = type_

    def calculate_hash_code(self):
        return 31 + (0 if self.type_ is None else hash(self.type_))

    def __eq__(self, other):
        return isinstance(other, Term) and hash(other) == hash(self) and self.do_equals(other)

    def get_type(self):
        return self.type_

    def do_equals(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.type_ is None:
            if other.type_ is not None:
                return False
        elif self.type_ != other.type_:
            return False
        return True
