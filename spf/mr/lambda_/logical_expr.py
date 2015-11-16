#!/usr/bin/env python


class LogicalExpressionComparator(object):
    def compare(self, o1, o2):
        return o1.do_equals(o2, {})

    def verify_arg_type(self, signature_type, arg_type):
        raise NotImplementedError()


class LogicalExpression(object):
    PARENTHESIS_CLOSE = ')'
    PARENTHESIS_OPEN = '('

    def __init__(self):
        self.hash_code_cache = -1
        self.hash_code_calculated = False

    def __hash__(self):
        if not self.hash_code_calculated:
            self.hash_code_cache = self.calculate_hash_code()
            self.hash_code_calculated = True
        return self.hash_code_cache

    def calculate_hash_code(self):
        raise NotImplementedError()

    def __str__(self):
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices
        return LogicLanguageServices.to_string(self)

    def __eq__(self, other):
        from spf.mr.lambda_.logic_language_services import LogicLanguageServices
        return isinstance(other, LogicalExpression) and \
               hash(self) == hash(other) and \
               LogicLanguageServices.is_equal(self, other)

    def do_equals(self, expr, mapping):
        raise NotImplementedError()

    def equals(self, expr, mapping):
        return expr is not None and hash(expr) == hash(self) and self.do_equals(expr, mapping)

    class Reader(object):
        @classmethod
        def is_valid(cls, string):
            raise NotImplementedError()

        @classmethod
        def read(cls, string, mapping, type_repository, type_comparator, reader):
            raise NotImplementedError()
