#!/usr/bin/env python
import re
from cStringIO import StringIO

from spf.mr.lambda_.logical_expr import LogicalExpressionComparator
from spf.mr.lambda_.ontology import Ontology
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.strict_type_comparator import StrictTypeComparator
from spf.mr.lambda_.primitivetypes.and_simplifier import AndSimplifier
from spf.mr.lambda_.primitivetypes.or_simplifier import OrSimplifier
from spf.mr.lambda_.primitivetypes.not_simplifier import NotSimplifier
from spf.mr.lambda_.term import Term
from spf.mr.lambda_.printer.logical_expr_to_string import LogicalExpressionToString
from spf.utils.lisp_reader import LispReader
from spf.utils.log import get_logger


class LogicLanguageServices(object):
    LOG = get_logger(__name__)
    INSTANCE = None

    def __init__(self, type_repository, numeral_type_name,
                 type_comparator, ontology,
                 conjunction_predicate,
                 disjunction_predicate,
                 negation_predicate,
                 index_increase_predicate,
                 true_constant,
                 false_constant,
                 printer):

        self.comparator = LogicalExpressionComparator()
        self.type_repository = type_repository
        self.ontology = ontology
        self.printer = printer
        self.numeral_type = None if numeral_type_name is None else type_repository.get_type(numeral_type_name)
        self.type_comparator = type_comparator

        # Basic predicates
        self.conjunction_predicate = conjunction_predicate
        self.disjunction_predicate = disjunction_predicate
        self.negation_predicate = negation_predicate
        self.index_increase_predicate = index_increase_predicate

        self.true_constant = true_constant
        self.false_constant = false_constant
        self.collapsible_constants = {true_constant, false_constant}

        self.simplifiers = {}
        self.set_simplifier(self.conjunction_predicate, AndSimplifier(), True)
        self.set_simplifier(self.disjunction_predicate, OrSimplifier(), True)
        self.set_simplifier(self.negation_predicate, NotSimplifier(), True)

        self.printer = LogicalExpressionToString.Printer()

    @classmethod
    def set_instance(cls, instance):
        cls.INSTANCE = instance

    @classmethod
    def compute_literal_typing(cls, predicate_type, arg_types):
        return Literal.compute_literal_typing(predicate_type,
                                              arg_types,
                                              cls.INSTANCE.type_comparator,
                                              cls.INSTANCE.type_repository)

    @classmethod
    def compute_literal_typing_for_args(cls, predicate_type, args):
        return Literal.compute_literal_typing(predicate_type,
                                              [arg.get_type() for arg in args],
                                              cls.INSTANCE.type_comparator,
                                              cls.INSTANCE.type_repository)

    @classmethod
    def get_comparator(cls):
        return cls.INSTANCE.comparator

    @classmethod
    def get_conjunction_predicate(cls):
        return cls.INSTANCE.conjunction_predicate

    @classmethod
    def get_disjunction_predicate(cls):
        return cls.INSTANCE.disjunction_predicate

    @classmethod
    def get_false(cls):
        return cls.INSTANCE.false_constant

    @classmethod
    def get_index_increase_predicate(cls):
        return cls.INSTANCE.index_increase_predicate

    @classmethod
    def get_negation_predicate(cls):
        return cls.INSTANCE.negation_predicate

    @classmethod
    def get_ontology(cls):
        return None if cls.INSTANCE is None else cls.INSTANCE.ontology

    @classmethod
    def get_true(cls):
        return cls.INSTANCE.true_constant

    @classmethod
    def get_type_comparator(cls):
        return cls.INSTANCE.type_comparator

    @classmethod
    def get_type_repository(cls):
        return cls.INSTANCE.type_repository

    @classmethod
    def to_string(cls, expr):
        return cls.INSTANCE.printer.to_string(expr)

    @classmethod
    def get_simplifier(cls, predicate):
        return cls.INSTANCE.simplifiers.get(predicate, None)

    @classmethod
    def is_equal(cls, expr1, expr2):
        return cls.INSTANCE.comparator.compare(expr1, expr2)

    @classmethod
    def is_coordination_predicate(cls, predicate):
        return predicate == cls.INSTANCE.conjunction_predicate or predicate == cls.INSTANCE.disjunction_predicate

    @classmethod
    def is_array_index_predicate(cls, predicate):
        # TODO, not implemented
        return False

    @classmethod
    def is_array_sub_predicate(cls, predicate):
        # TODO, not implemented
        return False

    def set_simplifier(self, predicate, simplifier, collapsible):
        if collapsible:
            self.collapsible_constants.add(predicate)
        self.simplifiers.update({predicate: simplifier})

    @classmethod
    def int_to_index_constant(cls, i):
        name = i + Term.TYPE_SEPARATOR + cls.INSTANCE.type_repository.get_index_type().get_name()
        if cls.INSTANCE.ontology is not None and cls.INSTANCE.ontology.contains(name):
            return cls.INSTANCE.ontology.get(name)
        else:
            return LogicalConstant.create_dynamic(name, cls.INSTANCE.type_repository.get_index_type())

    class Builder(object):
        def __init__(self, type_repository, type_comparator=StrictTypeComparator()):
            """

            :rtype: Builder
            """
            self.type_repository = type_repository
            self.type_comparator = type_comparator
            self.constants_files = set()
            self.numeral_type_name = None
            self.printer = None
            self.ontology_closed = False

        def set_numeral_type_name(self, numeral_type_name):
            self.numeral_type_name = numeral_type_name
            return self

        def set_printer(self, printer):
            self.printer = printer
            return self

        @classmethod
        def read_constants_from_file(cls, filename, type_repository):
            stripped_file = ''
            for line in open(filename, 'r'):
                line = line.strip()
                line = re.split('\\s*//', line)[0]
                if len(line) != 0:
                    stripped_file += line + " "

            ret = set()
            lisp_reader = LispReader(StringIO(stripped_file))
            while lisp_reader.has_next():
                expr = LogicalConstant.read(lisp_reader.next(), type_repository)
                ret.add(expr)
            return ret

        @classmethod
        def read_constants_from_files(cls, files, type_repository):
            ret = set()
            for filename in files:
                ret.update(cls.read_constants_from_file(filename, type_repository))
            return ret

        def add_constants_to_ontology(self, constants_file):
            if isinstance(constants_file, str):
                self.constants_files.add(constants_file)
            elif isinstance(constants_file, list):
                self.constants_files.union(constants_file)
            return self

        def close_ontology(self, closed):
            self.ontology_closed = closed
            return self

        def build(self):
            """
            Method for building a LogicLanguageServices

            :return: spf.mr.lambda_.logic_language_services.LogicLanguageServices
            """
            conjunction_predicate = LogicalConstant.read('and:<t*,t>', self.type_repository)
            disjunction_predicate = LogicalConstant.read('or:<t*,t>', self.type_repository)
            negation_predicate = LogicalConstant.read('not:<t,t>', self.type_repository)
            index_increase_predicate = LogicalConstant.read('inc:<%s,%s>' % (
                self.type_repository.get_index_type().get_name(),
                self.type_repository.get_index_type().get_name()), self.type_repository)

            true_constant = LogicalConstant.create('true:t', self.type_repository.get_truth_value_type())
            false_constant = LogicalConstant.create('false:t', self.type_repository.get_truth_value_type())

            if len(self.constants_files) == 0:
                ontology = None
                if self.ontology_closed:
                    raise RuntimeError('Closed ontology requested, but no logical constants were provided.')
            else:
                constants = self.read_constants_from_files(self.constants_files, self.type_repository)
                constants.add(conjunction_predicate)
                constants.add(disjunction_predicate)
                constants.add(negation_predicate)
                constants.add(index_increase_predicate)
                constants.add(true_constant)
                constants.add(false_constant)
                ontology = Ontology(constants, self.ontology_closed)

            return LogicLanguageServices(self.type_repository,
                                         self.numeral_type_name,
                                         self.type_comparator,
                                         ontology,
                                         conjunction_predicate,
                                         disjunction_predicate,
                                         negation_predicate,
                                         index_increase_predicate,
                                         true_constant,
                                         false_constant,
                                         self.printer)
