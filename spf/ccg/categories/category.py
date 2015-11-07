#!/usr/bin/env python

from spf.ccg.categories.syntax.syntax import SimpleSyntax
from spf.ccg.categories.syntax.complex_syntax import ComplexSyntax
from spf.ccg.categories.simple_category import SimpleCategory
from spf.ccg.categories.complex_category import ComplexCategory

class Category(object):
  @staticmethod
  def create(syntax_, semantics_=None):
    if isinstance(syntax_, SimpleSyntax):
      return SimpleCategory(syntax_, semantics_)
    elif isinstance(syntax_, ComplexSyntax):
      return ComplexCategory(syntax_, semantics_)
    else:
      raise RuntimeError('unsupported syntax type')
