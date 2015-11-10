#!/usr/bin/env python


class _Direction(object):
    def __init__(self, label):
        self.label = label

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if not isinstance(other, _Direction):
            return False
        if self.label is None:
            if other.label is not None:
                return False
        elif self.label != other.label:
            return False
        return True

    def __hash__(self):
        return 31 + (0 if self.label is None else hash(self.label))

    def __str__(self):
        return self.label

    def get_label(self):
        return self.label


class Direction(object):
    BACKWARD = _Direction("<")
    FORWARD = _Direction(">")
    STRING_MAPPING = {str(BACKWARD): BACKWARD, str(FORWARD): FORWARD}
    VALUES = [BACKWARD, FORWARD]

    @classmethod
    def value_of(cls, string):
        return cls.STRING_MAPPING.get(string, None)

    @classmethod
    def values(cls):
        return cls.VALUES


class RuleName(object):
    RULE_ADD = "+"

    def __init__(self, label, direction=None, order=0):
        self.label = label
        self.direction = direction
        self.order = order

    @staticmethod
    def create(label, direction=None, order=0):
        return RuleName(label, direction, order)

    @staticmethod
    def split_rule_label(label):
        if isinstance(label, RuleName):
            label = label.get_label()
        return label.split("\\%s" % RuleName.RULE_ADD)

    def __str__(self):
        return ("" if self.direction is None else str(self.direction)) + \
               self.label + \
               ("" if self.order == 0 else "%d" % self.order)

    def get_label(self):
        return self.label

    def get_direction(self):
        return self.direction

    def get_order(self):
        return self.order
