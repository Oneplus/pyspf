#!/usr/bin/env python

from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.primitivetypes.abstract_predicate_simplifier import AbstractPredicateSimplifier


class NotSimplifier(AbstractPredicateSimplifier):
    def simplify(self, expr):
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices

        if isinstance(expr, Literal):
            literal = expr

            if len(literal.get_arguments()) == 1:
                arg = literal.get_arguments()[0]
                if isinstance(arg, Literal) and arg.get_predicate() == literal.get_predicate():
                    # two not predicate, e.g. (not:<t,t> (not:<t,t> (foo:<e,t> bar:e))) -> (foo:<e,t> bar:e)
                    sub_not = arg
                    if len(sub_not.get_arguments()) == 1:
                        return sub_not.get_arguments()[0]
                elif arg == LogicLanguageServices.get_true():
                    # (not:<t,t> true:t) -> false:t
                    return LogicLanguageServices.get_false()
                elif arg == LogicLanguageServices.get_false():
                    # (not:<t,t> false:t) -> true:t
                    return LogicLanguageServices.get_true()
            return expr
        else:
            return expr