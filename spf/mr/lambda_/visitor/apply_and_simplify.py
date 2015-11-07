#!/usr/bin/env python

from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.visitor.get_variables import GetVariables
from spf.mr.lambda_.visitor.abstract_simplify import AbstractSimplify

class ApplyAndSimplify(AbstractSimplify):
  def __init__(self_, applied_to_arg_, root_variable_):
    super(ApplyAndSimplify, self_).__init__(False)
    self_.applied_once_already_ = False
    self_.applied_to_arg_ = applied_to_arg_
    self_.root_variable_ = root_variable_
    self_.arg_vars_ = GetVariables.of(self_.applied_to_arg_)

  @staticmethod
  def of(func_, arg_):
    if (not func_.get_type().is_complex() or
        not LogicLanguageServices.get_type_comparator().verfiy_arg_type(
          func_.get_type().get_domain(), arg_.get_type())):
      return None
    elif isinstance(func_, Lambda):
      lambda_ = func_
      variable_ = lambda_.get_argument()
      visitor = ApplyAndSimplify(arg_, variable_)
      visitor.visit(lambda_.get_body())
      return visitor.temp_return_
