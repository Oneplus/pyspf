#!/usr/bin/env python

from spf.mr.lambda_.logical_expr_builder import LogicalExpressionBuilder
from spf.ccg.categories.simple_category import SimpleCategory
from spf.ccg.categories.syntax.syntax import Syntax
from spf.ccg.categories.abstract_category_services import AbstractCategoryServices
from spf.mr.lambda_.visitor.is_type_consistent import IsTypeConsistent
from spf.mr.lambda_.visitor.simplify import Simplify
from spf.utils.log import get_logger


class LogicalExpressionCategoryServices(AbstractCategoryServices):
    LOG = get_logger(__name__)

    EMP = SimpleCategory(Syntax.EMPTY, None)
    EMPTY_CATEGORY_NP = SimpleCategory(Syntax.NP, None)
    EMPTY_CATEGORY_S = SimpleCategory(Syntax.S, None)

    def __init__(self, do_type_checking=False, validate_log_exps=False,
                 restrict_composition_direction=True):
        super(LogicalExpressionCategoryServices, self).__init__(restrict_composition_direction)
        self.do_type_checking = do_type_checking
        self.validate_log_exps = validate_log_exps
        self.LOG.info("Init :: %s: do_type_checking=%s, validate_log_exps=%s" % (
            self.__class__.__name__, do_type_checking, validate_log_exps))

    def apply_sem(self, function, argument):
        pass

    def compose_sem(self, primary, secondary, order):
        pass

    @classmethod
    def parse_semantics(cls, string, check_type=True):
        expr = LogicalExpressionBuilder.read(string)
        if check_type and not IsTypeConsistent.of(expr):
            raise RuntimeError("Semantic not well typed: %s" % string)
        return Simplify.of(expr)

    def __hash__(self):
        result = 31 + (1231 if self.do_type_checking else 1237)
        return result
