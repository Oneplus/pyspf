#!/usr/bin/env python

from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType, Option
from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.utils.lisp_reader import LispReader
from cStringIO import StringIO
import logging


class Literal(LogicalExpression):
    LOG = logging.getLogger(__name__)
    PREFIX = LogicalExpression.PARENTHESIS_OPEN

    def __init__(self, predicate, arguments, *args):
        """

        :param predicate:
        :param arguments:
        :param args:
        :return:
        """
        super(Literal, self).__init__()
        self.predicate = predicate
        self.arguments = arguments

        if len(args) == 0:
            from spf.mr.lambda_.logic_language_services import LogicLanguageServices
            type_comparator = LogicLanguageServices.get_type_comparator()
            type_repository = LogicLanguageServices.get_type_repository()
        elif len(args) == 2:
            type_comparator = args[0]
            type_repository = args[1]
        else:
            raise RuntimeError("Wrong number of arguments")

        if not predicate.get_type().is_complex():
            raise LogicalExpressionRuntimeError(
                'Predicate must have a complex type, not %s' % predicate.get_type())

        literal_typing = Literal.compute_literal_typing(
                self.predicate.get_type(),
                [arg.get_type() for arg in self.arguments],
                type_comparator,
                type_repository)
        self.type_ = None if literal_typing is None else literal_typing[0]

    @classmethod
    def compute_literal_typing(cls, predicate_type, arg_types, type_comparator, type_repository):
        """
        Input the predicate type, a list of argument types. Dealing with the <e,<e,t>>

        :rtype: object
        :param predicate_type:
        :param arg_types:
        :param type_comparator:
        :param type_repository:
        :return:
        """
        current_range = predicate_type
        current_num_args = 0
        implied_signature_types = []

        for i, arg_type in enumerate(arg_types):
            if not current_range.is_complex():
                break
            current_domain = current_range.get_domain()
            current_range = current_range.get_range()

            if (not type_comparator.verify_arg_type(current_domain, arg_type) and
                    isinstance(current_range, RecursiveComplexType) and
                    current_range.get_final_range().is_complex()):
                if current_num_args < current_range.get_min_args():
                    cls.LOG.debug('Recursive type %s requires a minimum of %d arguments, %d were provided.' % (
                        current_range.get_min_args(), current_range.get_min_args(), current_num_args))
                    return None
                current_domain = current_range.get_final_range().get_domain()
                current_range = current_range.get_final_range().get_range()
                current_num_args = 0

            if not type_comparator.verify_arg_type(current_domain, arg_type):
                cls.LOG.debug('Invalid argument type (%s) for signature type (%s)' % (arg_type, current_domain))
                return None

            implied_signature_types.append(current_domain)
            current_num_args += 1

            if i + 1 < len(arg_type) and not current_range.is_complex():
                cls.LOG.debug('Too many arguments for predicate of type %s: %s' % (predicate_type, arg_type))
                return None

        if isinstance(current_range, RecursiveComplexType):
            recursive_predicate_type = current_range
            if current_num_args >= recursive_predicate_type.get_min_args():
                return recursive_predicate_type.get_final_range(), implied_signature_types
            else:
                return (
                    type_repository.get_type_create_if_needed(
                        recursive_predicate_type.get_domain(),
                        recursive_predicate_type.get_final_range(),
                        Option(
                            recursive_predicate_type.is_order_sensitive(),
                            recursive_predicate_type.get_min_args() - current_num_args)),
                    implied_signature_types)
        else:
            return current_range, implied_signature_types

    def calculate_hash_code(self):
        result = 31
        if self.get_predicate_type().is_order_sensitive():
            result += (0 if self.arguments is None else hash(self.arguments))
        else:
            result *= 31
            for arg in self.arguments:
                result += hash(arg)
        result = result * 31 + (0 if self.predicate is None else hash(self.predicate))
        result = result * 31 + (0 if self.type_ is None else hash(self.type_))
        return result

    def do_equals(self, expr, mapping):
        pass

    def get_arguments(self):
        return self.arguments

    def get_predicate(self):
        return self.predicate

    def get_type(self):
        return self.type_

    def num_args(self):
        return len(self.arguments)

    def get_predicate_type(self):
        return self.predicate.get_type()

    class Reader(LogicalExpression.Reader):
        @classmethod
        def is_valid(cls, string):
            return string.startswith(Literal.PREFIX) and not string.startswith(Lambda.PREFIX)

        @classmethod
        def read(cls, string, mapping, type_repository, type_comparator, reader):
            try:
                lisp_reader = LispReader(StringIO(string))
                predicate_string = lisp_reader.next()
                predicate = reader.read(predicate_string, mapping, type_repository, type_comparator)

                arguments = []
                while lisp_reader.has_next():
                    element_string = lisp_reader.next()
                    argument = reader.read(element_string, mapping, type_repository, type_comparator)
                    arguments.append(argument)

                return Literal(predicate, arguments, type_comparator, type_repository)
            except Exception, e:
                Literal.LOG.error("Literal syntax error: %s" % string)
                raise e
