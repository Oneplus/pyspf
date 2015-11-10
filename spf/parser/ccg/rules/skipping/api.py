#!/usr/bin/env python
from spf.parser.ccg.rules.parse_rule_result import ParseRuleResult
from spf.parser.ccg.rules.rule_name import RuleName


class AbstractSkippingRule(object):
    RULE_LABEL = "skip"

    def __init__(self, direction, category_services):
        self.name = RuleName.create(self.RULE_LABEL, direction)
        self.empty_category = category_services.get_empty_category()

    def __eq__(self, other):
        """
        :type other: AbstractSkippingRule
        """
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False

        if self.category_services is None:
            if other.category_services is not None:
                return False
        elif self.category_services != other.category_services:
            return False

        if self.name is None:
            if other.name is not None:
                return False
        elif self.name != other.name:
            return False
        return True

    def get_name(self):
        return self.name

    def __hash__(self):
        result = 31 + (0 if self.empty_category is None else hash(self.empty_category))
        return 31 * result + (0 if self.name else hash(self.name))

    def __str__(self):
        return self.name

    def attempt_skipping(self, left, right, backward):
        right_category_empty = (right == self.empty_category)
        left_category_empty = (left == self.empty_category)

        if left_category_empty ^ right_category_empty:
            if left_category_empty and backward:
                return [ParseRuleResult(self.name, right)]
            elif right_category_empty and not backward:
                return [ParseRuleResult(self.name, left)]
        return []
