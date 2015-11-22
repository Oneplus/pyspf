#!/usr/bin/env python

import re
from spf.mr.language.type_.complex_type import ComplexType


class Option(object):
    DOMAIN_REPEAT_ORDER_INSENSITIVE = '*'
    DOMAIN_REPEAT_ORDER_SENSITIVE = '+'
    STRING_PATTERN = re.compile('(?P<type>.+?)(((?P<order>[*+])((?P<minargs>\\d+)|()))|())$')

    def __init__(self, order_sensitive, min_args):
        self.order_sensitive = order_sensitive
        self.min_args = min_args

    @staticmethod
    def parse(string):
        """
        parse string like t*10
        :param string:
        """
        m = Option.STRING_PATTERN.match(string)
        if m is not None:
            type_ = m.group('type')
            if m.group('order') is not None:
                order_sensitive = True if m.group('order') == '+' else False
                min_args = 2 if m.group('minargs') is None else int(m.group('minargs'))
                return type_, Option(order_sensitive, min_args)
            else:
                return type_, None
        else:
            raise Exception('Invalid type string')


class RecursiveComplexType(ComplexType):
    """ RecursiveComplexType is used to handle the type like <t*,t> """
    MIN_NUM_ARGUMENT = 2

    def __init__(self, label, domain, range_, *args):
        super(RecursiveComplexType, self).__init__(label, domain, range_)
        if len(args) == 2:
            self.order_sensitive = args[0]
            self.min_args = args[1]
        elif len(args) == 1:
            self.order_sensitive = args[0].order_sensitive
            self.min_args = args[0].min_args

    def get_final_range(self):
        return super(RecursiveComplexType, self).get_range()

    def get_min_args(self):
        return self.min_args

    def get_range(self):
        # TODO understanding this.
        return self

    def get_option(self):
        return Option(self.order_sensitive, self.min_args)

    def is_extending(self, other):
        return other is not None and \
                (other == self or (isinstance(other, RecursiveComplexType) and
                                    (self.min_args == other.min_args) and
                                    (self.order_sensitive == other.order_sensitive) and
                                    (self.get_domain().is_extending(other.get_domain())) and
                                    (self.get_final_range().is_extending(other.get_final_range())))
                 )

    def is_order_sensitive(self):
        return self.order_sensitive

    def __str__(self):
        return self.get_name()
