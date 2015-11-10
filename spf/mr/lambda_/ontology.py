#!/usr/bin/env python

from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.mr.lambda_.logical_const import LogicalConstant, WrappedConstant


class Ontology(object):
    def __init__(self, constants, closed):
        """
        The initializer

        :param constants: spf.mr.lambda_.logical_const.LogicalConstant
        :param closed:
        :return:
        """
        self.closed = closed
        self.constants = {}
        self.constants_by_name = {}

        for constant in constants:
            # TODO
            self.constants.update({WrappedConstant(constant): constant})
            self.constants_by_name.update({constant.get_name(): constant})

    def add(self, constant, force):
        """

        :param constant:
        :type constant: LogicalConstant
        :param force:
        :type force: bool
        :return:
        """
        if WrappedConstant(constant) not in self.constants:
            if force or not self.closed:
                self.constants.update({WrappedConstant(constant): constant})
                self.constants_by_name.update({constant.get_name(): constant})
            else:
                raise LogicalExpressionRuntimeError('Closed ontology. Failed to add %s' % str(constant))
        return self.get(constant.get_name())

    def get(self, constant):
        """

        :param constant:
        :type constant: LogicalConstant | str
        :return:
        """
        if isinstance(constant, LogicalConstant):
            return self.constants.get(WrappedConstant(constant), None)
        elif isinstance(constant, str):
            return self.constants_by_name.get(constant, None)
        else:
            raise LogicalExpressionRuntimeError('Not known type of input argument.')

    def contains(self, constant):
        """

        :param constant: spf.mr.lambda_.logical_const.LogicalConstant or str
        :return:
        """
        if isinstance(constant, LogicalConstant):
            return WrappedConstant(constant) in self.constants
        elif isinstance(constant, str):
            return constant in self.constants_by_name
        else:
            raise LogicalExpressionRuntimeError('Not known type of input argument.')

    def get_all_constants(self):
        """

        :return:
        """
        return self.constants.values()

    def get_all_predicates(self):
        """

        :return:
        :rtype: set [LogicalConstant]
        """
        predicates = set()
        for wrapped, constant in self.constants.iteritems():
            if constant.get_type().is_complex():
                predicates.add(constant)
        return predicates

    def get_or_add(self, constant, force):
        """

        :param constant:
        :type constant: LogicalConstant
        :param force:
        :type force: bool
        :return:
        """
        if self.contains(constant):
            return self.get(constant)
        else:
            return self.add(constant, force)

    def is_closed(self):
        return self.closed
