#!/usr/bin/env python

import re
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.utils.log import get_logger


class LogicalExpressionBuilder(object):
    LOG = get_logger(__name__)
    WHITE_SPACE = re.compile("\\s+")
    readers = [Lambda.Reader(), Literal.Reader(), LogicalConstant.Reader(), Variable.Reader()]

    @classmethod
    def read(cls, string, mapping=None, type_repository=None, type_comparator=None):
        if mapping is None:
            mapping = {}
        if type_repository is None:
            type_repository = LogicLanguageServices.get_type_repository()
        if type_comparator is None:
            type_comparator = LogicLanguageServices.get_type_comparator()

        flat_string = cls.WHITE_SPACE.sub(string, " ")
        try:
            for reader in cls.readers:
                if reader.is_valid(flat_string):
                    return reader.read(flat_string, mapping, type_repository, type_comparator, cls)
            raise AttributeError("Invalid logical expression syntax: %s" % string)
        except Exception, e:
            cls.LOG.error("Logic expression syntax error: %s" % flat_string)
            raise e
