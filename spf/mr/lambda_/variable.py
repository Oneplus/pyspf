#!/usr/bin/env python

from spf.mr.lambda_.term import Term
from spf.mr.lambda_.logical_expr import LogicalExpression
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
import logging


class Variable(Term):
    LOG = logging.getLogger(__name__)
    PREFIX = '$'

    def __init__(self, type_):
        super(Variable, self).__init__(type_)

    def accept(self, visitor):
        visitor.visit(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def do_equals(self, other, mapping):
        if self in mapping:
            return mapping[self] == other
        elif self not in mapping and other not in mapping.values():
            return other == self
        else:
            return False

    class Reader(LogicalExpression.Reader):
        @classmethod
        def is_valid(cls, string):
            return string.startswith(Variable.PREFIX)

        @classmethod
        def read(cls, string, mapping, type_repository, type_comparator, reader):
            """ Read variable from string like, $0:e
            :param string: str, the input string
            :param mapping: dict, the input map of variable
            :param type_repository:
            :param type_comparator:
            :param reader:
            """
            try:
                split = string.split(Term.TYPE_SEPARATOR)
                if len(split) == 2:
                    type_ = type_repository.get_type_create_if_needed(split[1])
                    if type_ is None:
                        raise LogicalExpressionRuntimeError('Invalid Type')
                    if split[0] in mapping:
                        raise LogicalExpressionRuntimeError(
                            'Variable overwrite is not supported, please supply unique names')
                    variable = Variable(type_)
                    mapping[split[0]] = variable
                    return variable
                else:
                    if string in mapping:
                        return mapping.get(string, None)
                    else:
                        raise LogicalExpressionRuntimeError('Undefined variable reference: %s' % string)
            except Exception, e:
                cls.LOG.error("Variable error: %s" % string)
                raise e
