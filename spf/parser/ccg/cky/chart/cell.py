#!/usr/bin/env python
from spf.utils.log import get_logger


class Cell(object):
    LOG = get_logger(__name__)

    def __init__(self, parse_step, start, end, is_complete_span):
        """

        :param CKYParseStepI parse_step:
        :param int start:
        :param int end:
        :param bool is_complete_span:
        :return:
        """
        self.is_complete_span = is_complete_span
        self.is_full_parse = parse_step.is_full_parse()