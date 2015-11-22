#!/usr/bin/env python

import logging
import sys
from spf.mr.lambda_.variable import Variable
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI


class IsTypeConsistent(LogicalExpressionVisitorI):
    """ Verify typing consistency across the logical form. """
    LOG = logging.getLogger(__name__)
    LOG.addHandler(logging.StreamHandler(sys.stderr))
    LOG.setLevel(logging.DEBUG)

    def __init__(self):
        self.variable_types = {}
        self.well_typed = True

    @staticmethod
    def of(expr_):
        visitor = IsTypeConsistent()
        visitor.visit(expr_)
        return visitor.well_typed

    def visit_lambda(self, lambda_):
        self.variable_types[lambda_.get_argument()] = lambda_.get_argument().get_type()
        lambda_.get_body().accept(self)
        self.variable_types.pop(lambda_.get_argument())

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        literal_typing = LogicLanguageServices.compute_literal_typing_for_args(
            literal.get_predicate_type(),
            literal.get_arguments())

        if literal_typing is None:
            raise RuntimeError('Failed to compute literal typing for. This should never '
                               'have happened, typing is computed during creation: %s' % literal)

        for signature_type, arg in zip(literal_typing[1], literal.get_arguments()):
            arg.accept(self)
            self.well_typed = self.well_typed and self.verify_literal_arg_typing(arg, signature_type)
            if not self.well_typed:
                self.LOG.debug('Literal %s is not well-typed. Mismatch between signature type '
                               '%s to argument %s.' % (literal, signature_type, arg))
                return

    def visit_logical_constant(self, logical_constant):
        return

    def visit_logical_expression(self, logical_expr):
        logical_expr.accept(self)

    def visit_variable(self, variable):
        return

    def verify_literal_arg_typing(self, arg, signature_type):
        if isinstance(arg, Variable):
            historical_type_ = self.variable_types.get(arg, None)
            if historical_type_ is None:
                self.variable_types.update({arg: arg.get_type()})
                return arg.get_type().is_extending_or_extended_by(signature_type)
            else:
                if signature_type.is_extending(historical_type_):
                    self.variable_types.update({arg: signature_type})
                    return True
                else:
                    return historical_type_.is_extending(signature_type)
        else:
            return signature_type.is_array() == arg.get_type().is_array() and \
                   arg.get_type().is_extending_or_extended_by(signature_type)
