#!/usr/bin/env python

from spf.mr.lambda_.logic_language_services import LogicLanguageServices

class FlexibleTypeComparator(object):
  def verify_arg_type(self_, signature_type_, arg_type_):
    return arg_type_.is_extending_or_extended_by(
        LogicLanguageServices.get_type_repository().generalize_type(signature_type_))
