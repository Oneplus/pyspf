#!/usr/bin/env python


class AbstractSyntax(object):
    """ Define interface for Syntax """
    def __hash__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def num_slashes(self):
        raise NotImplementedError()


class SimpleSyntax(AbstractSyntax):
    def __init__(self, label):
        self.label = label
        self.hash_code = self.calculate_hash_code()

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if not isinstance(other, SimpleSyntax):
            return False
        if self.label is None:
            if other.label is not None:
                return False
        elif self.label != other.label:
            return False
        return True

    def __hash__(self):
        return self.hash_code

    def __str__(self):
        return self.label

    def num_slashes(self):
        return 0

    def calculate_hash_code(self):
        return 31 + (0 if self.label is None else hash(self.label))


class Syntax(object):
    ADJ = SimpleSyntax('ADJ')
    AP = SimpleSyntax('AP')
    C = SimpleSyntax('C')
    DEG = SimpleSyntax('DEG')

    EMPTY = SimpleSyntax('EMPTY')

    N = SimpleSyntax('N')
    NP = SimpleSyntax('NP')
    PP = SimpleSyntax('PP')
    S = SimpleSyntax('S')

    STRING_MAPPING = {
        'ADJ': ADJ,
        'AP': AP,
        'C': C,
        'DEG': DEG,
        'EMPTY': EMPTY,
        'N': N,
        'NP': NP,
        'PP': PP,
        'S': S
    }

    VALUES = set(STRING_MAPPING.values())

    @classmethod
    def value_of(cls, name):
        """

        :param name:
        :rtype: SimpleSyntax
        """
        return cls.STRING_MAPPING.get(name, None)