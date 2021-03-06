#!/usr/bin/env python

from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.logical_expr import TypeComparatorI


class FlexibleTypeComparator(TypeComparatorI):
    def verify_arg_type(self, signature_type, arg_type):
        return arg_type.is_extending_or_extended_by(
            LogicLanguageServices.get_type_repository().generalize_type(signature_type))
