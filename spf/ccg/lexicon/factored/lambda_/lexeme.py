#!/usr/bin/env python
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.logical_const import LogicalConstant


class Lexeme(object):
    """
    Lexeme consists of
    * a list of string as the tokens
    * a list of constants
    * a list of type signatures as auxiliary type
    """
    def __init__(self, tokens, constants, origin):
        """

        :param tokens: The tokens of a lexeme entry
        :type tokens: list[str]
        :param constants:
        :type constants: list[LogicalConstant]
        :param origin:
        :type origin: str
        :return:
        """
        self.origin = origin
        self.constants = constants
        self.tokens = tokens
        self.type_signature = Lexeme.get_signature(constants)

    @staticmethod
    def get_signature(constants):
        return [LogicLanguageServices.get_type_repository().generalize_type(constant.get_type())
                for constant in constants]

    @staticmethod
    def read(line, origin):
        equals_index = line.find("=")
        tokens_string, constants_string = line[1: equals_index - 1], line[equals_index + 2: -1]
        tokens = tokens_string.split(", ")
        constants = [LogicalConstant.read(constant) for constant in constants_string.split()]
        return Lexeme(tokens, constants, origin)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if not isinstance(other, Lexeme):
            return False
        if self.constants is None:
            if other.constants is not None:
                return False
        elif self.constants != other.constants:
            return False
        if self.tokens is None:
            if other.tokens is not None:
                return False
        elif self.tokens != other.tokens:
            return False
        return True

    def get_constants(self):
        return self.constants

    def get_origin(self):
        return self.origin

    def get_tokens(self):
        return self.tokens

    def get_type_signature(self):
        return self.type_signature

    def __hash__(self):
        result = 31 + (0 if self.constants is None else hash(self.constants))
        return result * 31 + (0 if self.tokens is None else hash(self.tokens))

    def num_constants(self):
        return len(self.constants)

    def matches(self, tokens):
        return self.tokens == tokens

    def __str__(self):
        return "%s=%s" % (self.tokens, self.constants)
