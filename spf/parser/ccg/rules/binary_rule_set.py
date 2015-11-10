#!/usr/bin/env python


class BinaryRuleSet(object):
    def __init__(self, rules):
        """

        :param rules: ParseRules
        :return:
        """
        self.rules = rules

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.rules is None:
            if other.rules is not None:
                return False
        elif self.rules != other.rules:
            return False
        return True
