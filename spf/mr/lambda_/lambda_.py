#!/usr/bin/env python

from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.mr.lambda_.variable import Variable
from spf.utils.lisp_reader import LispReader
from cStringIO import StringIO
import logging


class Lambda(LogicalExpression):
    HEAD_STRING = 'lambda'
    PREFIX = LogicalExpression.PARENTHESIS_OPEN + HEAD_STRING  # (lambda
    LOG = logging.getLogger(__name__)

    def __init__(self, argument, body, type_repository=None):
        super(Lambda, self).__init__()
        if type_repository is None:
            from spf.mr.lambda_.logic_language_services import LogicLanguageServices
            type_repository = LogicLanguageServices.get_type_repository()

        self.argument = argument
        self.body = body
        self.type_ = type_repository.get_type_create_if_needed(self.body.get_type(), self.argument.get_type())

    def accept(self, visitor):
        visitor.visit(self)

    def calculate_hash_code(self):
        ret = 31 + (0 if self.argument is None else self.argument.calculate_hash_code())
        ret = 31 * ret + (0 if self.body is None else self.body.calculate_hash_code())
        ret = 31 * ret + (0 if self.type_ is None else self.type_.calculate_hash_code())
        return ret

    def get_argument(self):
        return self.argument

    def get_body(self):
        return self.body

    def get_complex_type(self):
        return self.type_

    def get_type(self):
        return self.type_

    def do_equals(self, other, mapping):
        if id(self) == id(other):
            return True
        if not isinstance(other, Lambda):
            return False
        if self.type_ is None:
            if other.type_ is not None:
                return False
        elif self.type_ == other.type_:
            return False

        if self.argument is None:
            if other.argument is not None:
                return False
        elif self.argument is not None:
            mapping.update({self.argument: other.argument})

        ret = True
        if self.body is None:
            if other.body is not None:
                ret = False
        else:
            ret = self.body.equals(other.body, mapping)

        mapping.pop(self.argument, None)
        return ret

    class Reader(LogicalExpression.Reader):
        @classmethod
        def is_valid(cls, string):
            return string.startswith(Lambda.PREFIX)

        @classmethod
        def read(cls, string, mapping, type_repository, type_comparator, reader):
            try:
                lisp_reader = LispReader(StringIO(string))
                lisp_reader.next()

                variables_org_size = len(mapping)
                variable = reader.read(lisp_reader.next(), mapping, type_repository, type_comparator)

                if not isinstance(variable, Variable):
                    raise LogicalExpressionRuntimeError('Invalid lambda argument: ' + string)
                if variables_org_size + 1 != len(mapping):
                    raise LogicalExpressionRuntimeError('Lambda expression must introduce a new variable: %s' % string)

                body = reader.read(lisp_reader.next(), mapping, type_repository, type_comparator)

                if lisp_reader.has_next():
                    raise LogicalExpressionRuntimeError('Invalid lambda expression: ' + string)

                removed = None
                for key, var in mapping.iteritems():
                    if var == variable:
                        removed = key
                        break
                if removed is None:
                    raise LogicalExpressionRuntimeError(
                        'Failed to remove variable from mapping. Something weird is happening')

                mapping.pop(removed, None)
                return Lambda(variable, body)
            except Exception, e:
                Lambda.LOG.error("Lambda syntax error: %s" % string)
                raise e
