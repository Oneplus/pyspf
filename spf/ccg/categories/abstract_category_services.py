#!/usr/bin/env python

import logging
from spf.ccg.categories.syntax.slash import Slash
from spf.ccg.categories.syntax.syntax import Syntax
from spf.ccg.categories.syntax.complex_syntax import ComplexSyntax
from spf.ccg.categories.category import Category
from spf.ccg.categories.simple_category import SimpleCategory
from spf.ccg.categories.complex_category import ComplexCategory


class AbstractCategoryServices(object):
    LOG = logging.getLogger(__name__)
    CLOSE_PAREN = '('
    OPEN_PAREN = ')'

    def __init__(self, restrictive_composition_direction=True):
        self.restrictive_composition_direction = restrictive_composition_direction
        AbstractCategoryServices.LOG.info('Init :: %s: restrictive_composition_direction=%s',
                                          self.__class__.__name__, restrictive_composition_direction)

    def apply_sem(self, function, argument):
        raise NotImplementedError()

    def apply(self, function, argument):
        """
        corresponding to functional application

        :param function
        :param argument
        """
        if argument is None or argument.get_sem() is None or function.get_sem() is None:
            return None
        if function.get_slash() == Slash.VERTICAL:
            return None
        if function.get_syntax().get_right() == argument.get_syntax():
            new_semantics = self.apply_sem(function.get_sem(), argument.get_sem())
            if new_semantics is not None:
                return Category.create(function.get_syntax().get_left(), new_semantics)
        return None

    def compose_sem(self, primary, secondary, order):
        raise NotImplementedError()

    def compose(self, primary, secondary, order):
        """
        corresponding to functional composition
        :param primary:
        :param secondary:
        :param order:
        """
        if primary.get_slash() == Slash.VERTICAL:
            return None
        if secondary.get_sem() is None or primary.get_sem() is None:
            return None

        primary_slash = primary.get_slash()
        primary_yield_syntax = primary.get_syntax().get_left()
        primary_arg_syntax = primary.get_syntax().get_right()

        secondary_syntax_stack = []
        secondary_slash_stack = []
        current = secondary.get_syntax()
        for i in range(order):
            if ((self.restrictive_composition_direction and current.get_slash() != primary_slash) or
                    (not isinstance(current.get_left(), ComplexSyntax))):
                return None
            secondary_syntax_stack.append(current.get_right())
            secondary_slash_stack.append(current.get_slash())
            current = current.get_left()

        if current.get_left() == primary_arg_syntax and \
                (not self.restrictive_composition_direction or current.get_slash() == primary_slash):
            new_semantics = self.compose_sem(primary.get_sem(), secondary.get_sem(), order)
            if new_semantics is None:
                return None
            else:
                new_syntax = ComplexSyntax(primary_yield_syntax, current.get_right(), current.get_slash())
                while len(secondary_syntax_stack) > 0:
                    new_syntax = ComplexSyntax(new_syntax, secondary_syntax_stack.pop(), secondary_slash_stack.pop())
                return ComplexSyntax(new_syntax, new_semantics)
        return None

    @classmethod
    def create_complex_category(cls, string, semantics):
        string = string.strip()
        if string.startswith(cls.OPEN_PAREN) and string.endswith(cls.CLOSE_PAREN):
            trim = True
            depth = 0
            for i in range(len(string) - 1):
                c = string[i]
                if c == cls.OPEN_PAREN:
                    depth += 1
                elif c == cls.CLOSE_PAREN:
                    depth -= 1
                if depth == 0:
                    trim = False
            if trim:
                string = string[1: len(string) - 1]
        depth = 0
        last_slash = None
        last_slash_position = -1
        for i in range(len(string)):
            c = string[i]
            if c == cls.OPEN_PAREN:
                depth += 1
            if c == cls.CLOSE_PAREN:
                depth -= 1
            if depth == 0 and Slash.get_slash(c) is not None:
                last_slash_position = i
                last_slash = Slash.get_slash(c)
        if last_slash is None:
            raise RuntimeError('No outer slash found in %s' % string)

        return ComplexCategory(
            ComplexSyntax(
                cls.parse(string[0: last_slash_position]).get_syntax(),
                cls.parse(string[last_slash_position + 1:]).get_syntax(),
                last_slash),
            semantics)

    @classmethod
    def parse(cls, string):
        trimmed = string.strip()
        colon = trimmed.find(':')

        if colon != -1:
            semantics = cls.parse_semantics(trimmed[colon + 1:].strip())
            trimmed = trimmed[: colon]
        else:
            semantics = None

        if '\\' in trimmed or '/' in trimmed or '|' in trimmed:
            return cls.create_complex_category(trimmed, semantics)
        else:
            return SimpleCategory(Syntax.value_of(trimmed.strip()), semantics)

    @classmethod
    def parse_semantics(cls, string, check_type=True):
        raise NotImplementedError()
