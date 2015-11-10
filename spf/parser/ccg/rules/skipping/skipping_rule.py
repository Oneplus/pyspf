#!/usr/bin/env python
from spf.parser.ccg.rules.rule_name import Direction
from spf.parser.ccg.rules.skipping.api import AbstractSkippingRule


class ForwardSkippingRule(AbstractSkippingRule):
    def __init__(self, category_services):
        super(ForwardSkippingRule, self).__init__(Direction.FORWARD, category_services)

    def apply(self, left, right):
        return self.attempt_skipping(left, right, False)


class BackwardSkippingRule(AbstractSkippingRule):
    def __init__(self, category_services):
        super(BackwardSkippingRule, self).__init__(Direction.BACKWARD, category_services)

    def apply(self, left, right):
        return self.attempt_skipping(left, right, True)
