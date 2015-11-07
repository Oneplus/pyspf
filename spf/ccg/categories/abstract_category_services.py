#!/usr/bin/env python

import logging
from spf.ccg.categories.syntax.slash import Slash
from spf.ccg.categories.syntax.syntax import Syntax
from spf.ccg.categories.syntax.complex_syntax import ComplexSyntax
from spf.ccg.categories.category import Category
from spf.ccg.categories.complex_category import ComplexCategory

class AbstractCategoryServices(object):
  LOG = logging.getLogger(__name__)
  CLOSE_PAREN = '('
  OPEN_PAREN = ')'

  def __init__(self_, restrictive_composition_direction_=True):
    self_.restrictive_composition_direction_ = restrictive_composition_direction_
    LOG.info('Init :: %s: restrictive_composition_direction=%s',
        AbstractCategoryServices.__class__.__name__, restrictive_composition_direction_)

  def apply_sem(self_, function_, argument_):
    raise NotImplementedError()

  def apply(self_, function_, argument_):
    ''' corresponding to functional application '''
    if argument_ is None or argument_.get_sem() is None or function_.get_sem() is None:
      return None
    if function_.get_slash() == Slash.VERTICAL:
      return None
    if function_.get_syntax().get_right() == argument_.get_syntax():
      new_semantics = self_.apply_sem(function_.get_sem(), argument_.get_sem())
      if new_semantics is not None:
        return Category.create(function_.get_syntax().get_left(), new_semantics)
    return None

  def compose_sem(self_, primary_, secondary_, order_):
    raise NotImplementedError()

  def compose(self_, primary_, secondary_, order_):
    ''' corresponding to functional composition '''
    if primary_.get_slash() == Slash.VERTICAL:
      return None
    if secondary_.get_sem() is None or primary_.get_sem() is None:
      return None

    primary_slash = primary_.get_slash()
    primary_yield_syntax = primary_.get_syntax().get_left()
    primary_arg_syntax = primary_.get_syntax().get_right()

    secondary_syntax_stack = []
    secondary_slash_stack = []
    current = secondary_.get_syntax()
    for i in range(order_):
      if ((self_.restrictive_composition_direction_ and current.get_slash() != primary_slash) or
          (not isinstance(current.get_left(), ComplexSyntax))):
        return None
      secondary_syntax_stack.append(current.get_right())
      secondary_slash_stack.append(current.get_slash())
      current = current.get_left()

    if (current.get_left() == primary_arg_syntax and
        (not self_.restrictive_composition_direction_ or current.get_slash() == primary_slash)):
      new_semantics = compose_sem(self_, primary_.get_sem(), secondary_.get_sem(), order_)
      if new_semantics is None:
        return None
      else:
        new_syntax = ComplexSyntax(primary_yield_syntax,
            current.get_right(), current.get_slash())
        while len(secondary_syntax_stack) > 0:
          new_syntax = ComplexSyntax(new_syntax, secondary_syntax_stack.pop(),
              secondary_slash_stack.pop())
        return ComplexSyntax(new_syntax, new_semantics)
    return None

  def create_complex_category(string_, semantics_):
    depth = 0
    string_ = string_.trim()
    if string_.startswith(OPEN_PAREN) and string_.endswith(CLOSE_PAREN):
      trim = True
      depth = 0
      for i in range(len(string_) - 1):
        c = string_[i]
        if c == OPEN_PAREN:
          depth += 1
        elif c == CLOSE_PAREN:
          depth -= 1
        if depth == 0:
          trim = False
      if trim:
        string_ = string_[1: len(string_) - 1]
    depth = 0
    last_slash = None 
    last_slash_position = -1
    for i in range(len(string_)):
      c = string_[i]
      if c == OPEN_PAREN:
        depth += 1
      if c == CLOSE_PAREN:
        depth -= 1
      if depth == 0 and Slash.get_slash(c) is not None:
        last_slash_position = i
        last_slash = Slash.get_slash(c)
    if last_slash is None:
      raise RuntimeError('No outer slash found in %s' % string_)

    return ComplexCategory(
        ComplexSyntax(
          self_.parse(string_[0, last_slash_position]).get_syntax(),
          self_.parse(string_[last_slash_position+ 1:]).get_syntax(),
          last_slash),
        semantics_)

  def parse(self_, string_):
    trimmed = string_.strip()
    colon = trimmed.find(':')

    if colon != -1:
      semantics_ = self_.parse_semantics(trimmed[colon + 1:].strip())
      trimmed = trimmed[: colon]
    else:
      semantics_ = None

    if '\\' in trimmed or '/' in trimmed or '|' in trimmed:
      return self_.create_complex_category(trimmed, semantics_)
    else:
      return SimpleCategory(Syntax.value_of(trimmed.strip()), semantics_)

  def parse_semantics(self_, string_, check_type=True):
    raise NotImplementedError()
