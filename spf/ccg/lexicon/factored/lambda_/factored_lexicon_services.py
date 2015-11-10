#!/usr/bin/env python
from spf.mr.lambda_.logic_language_services import LogicLanguageServices


class FactoredLexiconServices(object):
    unfactored_constants = set()

    @classmethod
    def is_factorable(cls, constant):
        return cls.do_is_factorable(constant)

    @classmethod
    def set(cls, constants):
        cls.unfactored_constants = set(constants)

    @classmethod
    def add_unfactored_constants(cls, constants):
        cls.unfactored_constants.update(constants)

    @classmethod
    def do_is_factorable(cls, constant):
        return not LogicLanguageServices.is_coordination_predicate(constant) and \
               not LogicLanguageServices.is_array_index_predicate(constant) and \
               not LogicLanguageServices.is_array_sub_predicate(constant) and \
               LogicLanguageServices.get_type_repository().get_index_type() != constant.get_type() and \
               constant not in cls.unfactored_constants

