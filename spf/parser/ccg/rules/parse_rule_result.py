#!/usr/bin/env python


class ParseRuleResult(object):
    def __init__(self, rule_name, result_category):
        self.rule_name = rule_name
        self.result_category = result_category

    def get_result_category(self):
        return self.result_category

    def __str__(self):
        return "%s -> %s" % (self.rule_name, self.result_category)