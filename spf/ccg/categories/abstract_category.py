#!/usr/bin/env python


class AbstractCategory(object):
    def __init__(self, semantics):
        self.hash_code_cache = None
        self.hash_code_calculated = False
        self.semantics = semantics

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if not isinstance(other, AbstractCategory):
            return False
        if self.semantics is None:
            if other.semantics is not None:
                return False
        elif self.semantics != other.semantics:
            return False
        return True

    def clone_with_new_semantics(self, new_semantics):
        raise NotImplementedError()

    def equals_no_sem(self, other):
        raise NotImplementedError()

    def get_sem(self):
        return self.semantics

    def __hash__(self):
        if not self.hash_code_calculated:
            self.hash_code_cache = self.calculate_hash_code()
            self.hash_code_calculated = True
        return self.hash_code_cache

    def matches(self, c):
        raise NotImplementedError()

    def matches_no_sem(self, c):
        raise NotImplementedError()

    def num_slashes(self):
        raise NotImplementedError()

    def calculate_hash_code(self):
        if self.semantics is None:
            return 0
        return self.syntax_hash() + hash(self.semantics)

    def syntax_hash(self):
        raise NotImplementedError()
