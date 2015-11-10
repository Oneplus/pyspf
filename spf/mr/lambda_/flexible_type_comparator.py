#!/usr/bin/env python

from spf.mr.lambda_.logic_language_services import LogicLanguageServices


class FlexibleTypeComparator(object):
    def verify_arg_type(self, signature_type, arg_type):
        return arg_type.is_extending_or_extended_by(
            LogicLanguageServices.get_type_repository().generalize_type(signature_type))
