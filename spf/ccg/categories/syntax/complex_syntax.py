#!/usr/bin/env python

from spf.ccg.categories.syntax.syntax import AbstractSyntax


class ComplexSyntax(AbstractSyntax):
    def __init__(self, left, right, slash):
        self.left = left
        self.right = right
        self.n_slashes = left.num_slashes() + right.num_slashes() + 1
        self.slash = slash
        self.hash_code = self.calculate_hash_code()
        self.string = ComplexSyntax.compute_syntax_string(left, right, slash)

    @staticmethod
    def compute_syntax_string(left, right, slash):
        ret = str(left) + str(slash)
        if isinstance(right, ComplexSyntax):
            ret += '(%s)' % str(right)
        else:
            ret += str(right)
        return ret

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_slash(self):
        return self.slash

    def num_slashes(self):
        return self.n_slashes

    def calculate_hash_code(self):
        ret = 31 + (0 if self.left is None else hash(self.left))
        ret += 31 * ret + (0 if self.right is None else hash(self.right))
        ret += 31 * ret + (0 if self.slash is None else hash(self.slash))
        return ret

    def __hash__(self):
        return self.hash_code

    def __str__(self):
        return self.string
