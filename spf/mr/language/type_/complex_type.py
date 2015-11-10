#!/usr/bin/env python

from spf.mr.language.type_.type_ import Type


class ComplexType(Type):
    COMPLEX_TYPE_CLOSE_PAREN = '>'
    COMPLEX_TYPE_OPEN_PAREN = '<'
    COMPLEX_TYPE_SEP = ','

    def __init__(self, label, domain, range_):
        super(ComplexType, self).__init__(label)
        self.domain = domain
        self.range_ = range_

    @staticmethod
    def compose_string(range_, domain, option):
        ret = '<{domain}{option},{range}>'.format(
            domain=str(domain),
            option=('' if option is None else str(option)),
            range=str(range_))
        return ret

    @staticmethod
    def create(string_, domain, range_, option):
        if option is None:
            return ComplexType(string_, domain, range_)
        else:
            raise NotImplementedError('create RecursiveComplexType is not implemented')

    def get_domain(self):
        return self.domain

    def get_range(self):
        return self.range_

    def is_array(self):
        return False

    def is_complex(self):
        return True

    def is_extending(self, other):
        """
        Whether a class is extending other depends on its range and its domain, if both its range and its
        domain are extending other, it should be extending other.
        :param other:
        :return:
        """
        return other is not None \
               and (self == other or (self.domain.is_extending(other.get_domain())
                                      and self.range_.is_extending(other.get_range())))

    def is_extending_or_extended_by(self, other):
        return self.is_extending(other) or other.is_extending(self)

    def is_order_sensitive(self):
        return True

    def __str__(self):
        return self.get_name()
