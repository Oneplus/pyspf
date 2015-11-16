#!/usr/bin/env python
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.visitor.api import LogicalExpressionVisitorI
from spf.mr.lambda_.lambda_ import Lambda
from spf.mr.lambda_.literal import Literal


class Placeholders(object):
    def __init__(self, abstractor, do_maximal=False):
        self.abstractor = abstractor
        self.maximal = do_maximal
        self.originals = []
        self.placeholders = []

    def add(self, original):
        self.originals.append(original)
        placeholder = self.make_constant(original.get_type())

    def concat(self, other):
        self.originals.extend(other.originals)
        self.placeholders.extend(other.placeholders)

    def is_maximal(self):
        return self.maximal

    def __str__(self):
        return "%s%s%s" % (self.originals, " M-> " if self.maximal else " -> ", self.placeholders)

    def __len__(self):
        return len(self.originals)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.abstractor != other.abstractor:
            return False
        if self.originals is None:
            if other.originals is not None:
                return False
        elif self.originals != other.originals:
            return False
        if self.placeholders is None:
            if other.placeholders is not None:
                return False
        elif self.placeholders != other.placeholders:
            return False
        return True

    def __hash__(self):
        result = 31 * 1 + 0 if self.originals is None else hash(self.originals)
        result = 31 * result + 0 if self.placeholders is None else hash(self.placeholders)
        return result

    def make_constant(self, type_):
        general_type = LogicLanguageServices.get_type_repository().generalize_type(type_)
        counters = self.abstractor.counters
        name = "#%d%s" % (counters.get(general_type) if general_type in counters else 0, general_type)
        return LogicalConstant.create_dynamic(LogicalConstant.make_name(name, general_type), general_type)


class AbstractConstants(LogicalExpressionVisitorI):
    def __init__(self, do_maximal, do_partial, partial_max_constants):
        self.do_maximal = do_maximal
        self.do_partial = do_partial
        self.partial_max_constants = partial_max_constants
        self.temp_return = None

    @staticmethod
    def of(expr, get_maximal, get_partial, partial_max_constants):
        visitor = AbstractConstants(get_maximal, get_partial, partial_max_constants)
        visitor.visit(expr)
        return set([(_, expr) for _, expr in visitor.temp_return if _.is_maximal() or len(_) != 0])

    @staticmethod
    def get_and_remove_maximal(pairs):
        ret = [(first, second) for first, second in pairs if first.is_maximal()][0]
        # Tricky to make it revise the input argument
        pairs[:] = [(first, second) for first, second in pairs if not first.is_maximal()]
        return ret

    def visit_lambda(self, lambda_):
        lambda_.get_body().accept(self)
        for i, (_, expr) in enumerate(self.temp_return):
            if expr is not None:
                new_body = expr
                if new_body == lambda_.get_body():
                    self.temp_return[i] = _, new_body
                else:
                    self.temp_return[i] = _, Lambda(lambda_.get_argument(), new_body)

    def visit_literal(self, literal):
        literal.get_predicate().accept(self)
        predicate_return = self.temp_return
        args = literal.get_arguments()
        args_returns = []

        if not literal.get_predicate_type().is_order_sensitive():
            payload = sorted(args, key=lambda x: hash(x))
        else:
            payload = args

        for arg in payload:
            arg.accept(self)
            args_returns.append(self.temp_return)

        self.temp_return = []
        if self.do_maximal:
            predicate_pair = self.get_and_remove_maximal(predicate_return)
            argument_pairs = [self.get_and_remove_maximal(arg) for arg in args_returns]
            placeholder = predicate_pair[0]
            args_changed = False
            new_args = []
            for i, (first, second) in enumerate(argument_pairs):
                placeholder.concat(first)
                new_args.append(second)
                if args[i] != second:
                    args_changed = True
            if args_changed or predicate_pair[1] != literal.get_predicate():
                self.temp_return.append((
                    placeholder,
                    Literal(
                        literal.get_predicate() if predicate_pair[1] == literal.get_predicate() else predicate_pair[1],
                        new_args)
                ))
            else:
                self.temp_return.append((placeholder, literal))

        if self.do_partial:
            pass

    def visit_variable(self, variable):
        pass

    def visit_logical_expression(self, logical_expr):
        pass

    def visit_logical_constant(self, logical_constant):
        pass


class LexicalTemplate(object):
    def __init__(self, constants, template, origin):
        self.origin = origin
        self.constants = constants
        self.template = template
        self.type_signature = [constant.get_type() for constant in constants]

    def do_factoring(self, input_category, do_maximal, do_partial, max_constants_in_partial, origin):
        pass
