#!/usr/bin/env python
from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.language.type_.recursive_complex_type import RecursiveComplexType


class ComplexTypeBuilder(object):
    @staticmethod
    def create(string, domain, range_, option):
        if option is None:
            return ComplexType(string, domain, range_)
        else:
            return RecursiveComplexType(string, domain, range_, option)


