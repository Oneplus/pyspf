#!/usr/bin/env python
from spf.parser.ccg.cky.chart.api import CKYParseStepI


class CKYLexcialStep(CKYParseStepI):
    def __init__(self, root, lexical_entry, is_full_parse, rule_name, model):
        """

        :param Category root:
        :param LexicalEntry lexical_entry:
        :param bool is_full_parse:
        :param RuleName rule_name:
        :param Model model:
        :return:
        """
        super(CKYLexcialStep, self).__init__(
            root=root, left_child=None, right_child=None,
            is_full_parse=is_full_parse, rule_name=rule_name, model=model
        )

    def get_lexical_entry(self):
        return self.lexical_entry