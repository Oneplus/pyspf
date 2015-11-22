#!/usr/bin/env python

from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.term import Term
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.visitor.get_variables import GetVariables
from spf.mr.lambda_.visitor.abstract_simplify import SimplifyI
from spf.mr.lambda_.visitor.replace_variables_if_present import ReplaceVariablesIfPresent
from spf.mr.lambda_.visitor.simplify import Simplify


class ApplyAndSimplify(SimplifyI):
    def __init__(self, applied_to_arg, root_variable):
        """

        :param applied_to_arg: spf.mr.lambda_.logical_expr.LogicalExpression,
        :param root_variable: spf.mr.lambda_.logical_expr.LogicalExpression,
        :return:
        """
        super(ApplyAndSimplify, self).__init__(False)
        self.applied_once_already = False
        self.applied_to_arg = applied_to_arg
        self.root_variable = root_variable
        self.old_variables_to_new = {}
        self.arg_vars = GetVariables.of(self.applied_to_arg)

    @staticmethod
    def of(func, arg):
        """

        :param func:
        :param arg:
        :return:
        """
        if (not func.get_type().is_complex() or
                not LogicLanguageServices.get_type_comparator().verfiy_arg_type(
                    func.get_type().get_domain(), arg.get_type())):
            return None
        elif isinstance(func, Lambda):
            lambda_ = func
            variable = lambda_.get_argument()
            visitor = ApplyAndSimplify(arg, variable)
            visitor.visit(lambda_.get_body())
            return visitor.temp_return
        elif isinstance(func, Literal):
            return Simplify.of(ApplyAndSimplify.literal_application(func, arg))
        elif isinstance(func, Term):
            return Simplify.of(ApplyAndSimplify.term_application(func, arg))
        else:
            raise LogicalExpressionRuntimeError('Impossible condition: unhandled logical expression object.')

    @staticmethod
    def should_consume_args(new_predicate):
        return (new_predicate.get_type().is_complex() and
                not isinstance(new_predicate, LogicalConstant) and
                not isinstance(new_predicate, Variable))

    @staticmethod
    def literal_application(literal, arg):
        new_args = [arg for arg in literal.get_arguments()]
        new_args.append(ReplaceVariablesIfPresent.of(arg, GetVariables.of(literal)))
        return Literal(literal.get_predicate(), new_args)

    @staticmethod
    def term_application(expr, arg):
        new_args = [arg]
        return Literal(Variable(expr.get_type()) if expr in GetVariables.of(arg) else expr, new_args)

    def visit_literal(self, literal):
        """
        Basiclly, it seems erase all the last parameter
        :param literal: spf.mr.lambda_.literal.Literal, the input literal
        :return:
        """
        literal.get_predicate().accept(self)
        simplified_predicate = self.temp_return

        new_args = []
        args_changed = False
        for arg in literal.get_arguments():
            arg.accept(self)
            if self.temp_return != arg:
                args_changed = True
            new_args.append(self.temp_return)

        if args_changed:
            simplified_args = new_args
        else:
            simplified_args = literal.get_arguments()

        new_predicate = simplified_predicate
        if self.should_consume_args(new_predicate):
            change_due_to_lambda_application = False
            for arg in simplified_args:
                if not self.should_consume_args(new_predicate):
                    break
                apply_result = ApplyAndSimplify.of(new_predicate, arg)
                if apply_result is None:
                    break
                else:
                    new_predicate = apply_result
                    change_due_to_lambda_application = True

            if change_due_to_lambda_application:
                final_args = None
            else:
                final_args = simplified_args
        else:
            final_args = simplified_args

        if new_predicate != literal.get_predicate() or final_args != literal.get_arguments():
            if len(final_args) == 0:
                new_expr = new_predicate
            else:
                new_expr = Literal(new_predicate, final_args)
        else:
            new_expr = literal

        self.temp_return = new_expr

        if len(final_args) > 0:
            simplifier = LogicLanguageServices.get_simplifier(new_predicate)
            if simplifier is not None:
                simplified_expr = simplifier.simplify(new_expr)
            if simplified_expr != new_expr:
                self.temp_return = simplified_expr
                return

    def visit_variable(self, variable):
        if variable == self.root_variable:
            if self.applied_once_already:
                pass