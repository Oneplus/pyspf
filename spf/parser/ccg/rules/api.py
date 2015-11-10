#!/usr/bin/env python


class UnaryParseRuleI(object):
    def apply(self, category):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()

    def is_valid_argument(self, category):
        raise NotImplementedError()


class BinaryParseRuleI(object):
    def __eq__(self, other):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()

    def apply(self, left, right):
        raise NotImplementedError()
