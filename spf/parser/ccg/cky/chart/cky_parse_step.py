#!/usr/bin/env python
from spf.parser.ccg.cky.chart.api import CKYParseStepI


class CKYParseStep(CKYParseStepI):
    def __init__(self, root, left_child, right_child, is_full_parse, rule_name, model):
        super(CKYParseStep, self).__init__(root, left_child, right_child, is_full_parse, rule_name, model)