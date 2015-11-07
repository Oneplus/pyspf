#!/usr/bin/env python

import logging

from spf.ccg.categories.simple_category import SimpleCategory
from spf.ccg.categories.syntax.syntax import Syntax
from spf.ccg.categories.abstract_category_services import AbstractCategoryServices

class LogicalExpressionCategoryServices(AbstractCategoryServices):
  LOG = logging.getLogger(__name__)
  EMP = SimpleCategory(Syntax.EMPTY, None)
  EMPTY_CATEGORY_NP = SimpleCategory(Syntax.NP, None)
  EMPTY_CATEGORY_NP = SimpleCategory(Syntax.S, None)

  def __init__(self_, do_type_checking_=False, validate_log_exps_=False,
      restrict_composition_direction_=True):
    super(LogicalExpressionCategoryServices, self_).__init__(restrict_composition_direction_)
    self_.do_type_checking_ = do_type_checking_
    self_.validate_log_exps_ = validate_log_exps_
    LOG.info('Init :: %s: do_type_checking=%s, validate_log_exps=%s' % (
      LogicalExpressionCategoryServices.get_simple_name(), do_type_checking_,
      validate_log_exps_))

  def apply_sem(self_, function_, argument_):
    pass

  def compose_sem(self_, primary_, secondary_):
    pass
