#!/usr/bin/env python

from spf.ccg.categories.syntax.syntax import SimpleSyntax
from spf.ccg.categories.syntax.complex_syntax import ComplexSyntax
from spf.ccg.categories.simple_category import SimpleCategory
from spf.ccg.categories.complex_category import ComplexCategory


class Category(object):
    @staticmethod
    def create(syntax, semantics=None):
        if isinstance(syntax, SimpleSyntax):
            return SimpleCategory(syntax, semantics)
        elif isinstance(syntax, ComplexSyntax):
            return ComplexCategory(syntax, semantics)
        else:
            raise RuntimeError('unsupported syntax type')
