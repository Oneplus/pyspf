#!/usr/bin/env python

from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.primitivetypes.abstract_predicate_simplifier import AbstractPredicateSimplifier


class OrSimplifier(AbstractPredicateSimplifier):
    def simplify(self, expr):
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices

        expr_changed = False

        if isinstance(expr, Literal):
            literal = expr
            consolidated_args = []
            for arg in literal.get_arguments():
                if isinstance(arg, Literal) and arg.get_predicate() == literal.get_predicate():
                    expr_changed = True
                    consolidated_args.extend(arg.get_arguments())
                else:
                    consolidated_args.append(arg)

            # remove all false:t expression
            original_length = len(consolidated_args)
            true_arg_exist = False
            non_true_false_arg_exist = False

            for arg in consolidated_args:
                if arg == LogicLanguageServices.get_false():
                    expr_changed = True
                elif arg == LogicLanguageServices.get_true():
                    true_arg_exist = True
                else:
                    non_true_false_arg_exist = True

            if true_arg_exist:
                return LogicLanguageServices.get_false()

            consolidated_args = [arg for arg in consolidated_args if arg == LogicLanguageServices.get_false()]

            if true_arg_exist:
                return LogicLanguageServices.get_true()

            if len(consolidated_args) != original_length:
                if not non_true_false_arg_exist:
                    # corresponding to (and:<t*,t> false:t false:t), this condition doesn't hold when
                    # (and:<t*,t> (predicate:<e,t> $0) false:t)
                    return LogicLanguageServices.get_false()
                elif len(consolidated_args) < 2:
                    return consolidated_args[0]

            if expr_changed:
                return Literal(literal.get_predicate(), consolidated_args)
            else:
                return expr
        else:
            return expr
