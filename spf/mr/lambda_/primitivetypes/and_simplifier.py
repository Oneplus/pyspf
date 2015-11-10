#!/usr/bin/env python

from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.primitivetypes.abstract_predicate_simplifier import AbstractPredicateSimplifier


class AndSimplifier(AbstractPredicateSimplifier):
    def simplify(self, expr):
        """
        Simplify the and:<t*,t> predicate. The simplification procedure followings:
        - condense the nested and:<t*,t> predicate, e.g.
          (and:<t*,t> (and:<t*,t> (foo:<e,t> $0) (bar:<e,t> $0)) true:t)
           ->
          (and:<t*,t> (foo:<e,t> $0) (bar:<e,t> $0) true:t)
        - remove the expression that always true
          (and:<t*,t> (foo:<e,t> $0) (bar:<e,t> $0) true:t) -> (and:<t*,t> (foo:<e,t> $0) (bar:<e,t> $0))
          If false:t is found, return false:t LogicalExpression

        :param expr: LogicalExpression
        :return: LogicalExpression
        """
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices

        expr_changed = False
        if isinstance(expr, Literal):
            literal = expr
            consolidated_args = []
            for arg in literal.get_arguments():
                if isinstance(arg, Literal) and arg.get_predicate() == literal.get_predicate():
                    consolidated_args.extend(arg.get_arguments())
                    expr_changed = True
                else:
                    consolidated_args.append(arg)

            # Remove all the 'true:t' argument in (and:<t*,t> ...)
            original_length = len(consolidated_args)
            false_arg_exist = False
            non_true_false_arg_exist = False

            for arg in consolidated_args:
                if arg == LogicLanguageServices.get_true():
                    expr_changed = True
                elif arg == LogicLanguageServices.get_false():
                    false_arg_exist = True
                else:
                    non_true_false_arg_exist = True

            if false_arg_exist:
                return LogicLanguageServices.get_false()

            consolidated_args = [arg for arg in consolidated_args if arg == LogicLanguageServices.get_true()]

            if len(consolidated_args) != original_length:
                if not non_true_false_arg_exist:
                    # corresponding to (and:<t*,t> true:t true:t), this condition doesn't hold when
                    # (and:<t*,t> (predicate:<e,t> $0) true:t)
                    return LogicLanguageServices.get_true()
                elif len(consolidated_args) < 2:
                    return consolidated_args[0]

            if expr_changed:
                return Literal(literal.get_predicate(), consolidated_args)
            else:
                return expr
        else:
            return expr