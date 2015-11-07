#!/usr/bin/env python

from spf.mr.lambda_.ontology import Ontology
from spf.mr.lambda_.literal import Literal
from spf.mr.lambda_.term import Term
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.lambda_.logical_expr_runtime_error import LogicalExpressionRuntimeError
from spf.mr.lambda_.logical_expr_comparator import LogicalExpressionComparator
from spf.mr.lambda_.strict_type_comparator import StrictTypeComparator
from spf.mr.language.type_.type_ import Type
from spf.mr.language.type_.complex_type import ComplexType
from spf.mr.language.type_.type_repository import TypeRepository
from spf.utils.lisp_reader import LispReader

import logging
import re

class LogicLanguageServices(object):
  LOG = logging.getLogger(__name__)

  type_repository_ = None
  comparator_ = LogicalExpressionComparator()
  ontology_ = None
  printer_ = None
  numeral_type_ = None
  type_comparator_ = None

  conjunction_predicate_ = None
  disjunction_predicate_ = None
  negation_predicate_ = None
  index_increase_predicate_ = None

  true_constant_ = None
  false_constant_ = None
  collapsible_constants_ = None

  def __init__(self_, type_repository_, numeral_type_name_,
      type_comparator_, ontology_,
      conjunction_predicate_,
      disjunction_predicate_,
      negation_predicate_,
      index_increase_predicate_,
      true_constant_,
      false_constant_,
      printer_):
    LogicLanguageServices.type_repository_ = type_repository_
    LogicLanguageServices.ontology_ = ontology_
    LogicLanguageServices.printer_ = printer_
    LogicLanguageServices.numeral_type_ = (None if numeral_type_name_ is None else
        type_repository_.get_type(numeral_type_name_))
    LogicLanguageServices.type_comparator_ = type_comparator_

    # Basic predicates
    LogicLanguageServices.conjunction_predicate_ = conjunction_predicate_
    LogicLanguageServices.disjunction_predicate_ = disjunction_predicate_
    LogicLanguageServices.negation_predicate_ = negation_predicate_
    LogicLanguageServices.index_increase_predicate_ = index_increase_predicate_

    # set simplifier
    # 1.
    # 2.

    LogicLanguageServices.true_constant_ = true_constant_
    LogicLanguageServices.false_constant_ = false_constant_
    LogicLanguageServices.collapsible_constants_ = set([true_constant_, false_constant_])

  @staticmethod
  def compute_literal_typing(predicate_type, arg_types):
    return Literal.compute_literal_typing(predicate_type,
        arg_types,
        LogicLanguageServices.type_comparator_,
        LogicLanguageServices.type_repository_)

  @staticmethod
  def compute_literal_typing_from_args(predicate_type, args):
    return Literal.compute_literal_typing(predicate_type,
        [arg.get_type() for arg in args],
        LogicLanguageServices.type_comparator_,
        LogicLanguageServices.type_repository_)

  @staticmethod
  def get_comparator():
    return LogicLanguageServices.comparator

  @staticmethod
  def get_conjunction_predicate():
    return LogicLanguageServices.conjunction_predicate_

  @staticmethod
  def get_disjunction_predicate():
    return LogicLanguageServices.disjunction_predicate_

  @staticmethod
  def get_false():
    return LogicLanguageServices.false_constant_

  @staticmethod
  def get_index_increase_predicate():
    return LogicLanguageServices.index_increase_predicate_

  @staticmethod
  def get_ontology():
    return LogicLanguageServices.ontology_

  @staticmethod
  def get_true():
    return LogicLanguageServices.true_constant_

  @staticmethod
  def get_type_comparator():
    return LogicLanguageServices.type_comparator_

  @staticmethod
  def get_type_repository():
    return LogicLanguageServices.type_repository_

  class Builder(object):
    def __init__(self_, type_repository_, type_comparator_=StrictTypeComparator()):
      self_.type_repository_ = type_repository_
      self_.type_comparator_ = type_comparator_
      self_.constants_files_ = set()
      self_.numeral_type_name_ = None
      self_.printer_ = None
      self_.ontology_closed_ = False

    def set_numeral_type_name(self_, numeral_type_name_):
      self_.numeral_type_name_ = numeral_type_name_
      return self_

    def set_printer(self_, printer_):
      self_.printer_ = printer_
      return self_

    @classmethod
    def read_constants_from_file(self_, file_, type_repository_):
      stripped_file = ''
      for line in open(file_, 'r'):
        line = line.strip()
        line = re.split('\\s*//')[0]
        if len(line) == 0:
          stripped_file += line

      ret = set()
      lisp_reader = LispReader(stripped_file)
      while lisp_reader.has_next():
        expr = LogicalConstant.read(lisp_reader.next(), type_repository_)
        ret.add(expr)
      return ret

    @classmethod
    def read_constants_from_files(self_, files, type_repository_):
      ret = set()
      for file_ in files:
        ret.update(self_.read_constants_from_file(file_, type_repository_))
      return ret

    def add_constants_to_ontology(self_, constants_file):
      if isinstance(constants_file, str):
        self_.constants_files_.add(constants_file)
      elif isinstance(constants_file, list):
        self_.constants_files_.union(constants_file)
      return self_

    def close_ontology(self_, is_closed_):
      self_.is_closed_ = is_closed_
      return self_

    def build(self_):
      conjunction_predicate_ = LogicalConstant.read('and:<t*,t>', self_.type_repository_)
      disjunction_predicate_ = LogicalConstant.read('or:<t*,t>', self_.type_repository_)
      negation_predicate_  = LogicalConstant.read('not:<t,t>', self_.type_repository_)
      index_increase_predicate_ = LogicalConstant.read('inc:<%s,%s>' % (
        self_.type_repository_.get_index_type().get_name(),
        self_.type_repository_.get_index_type().get_name()), self_.type_repository_)

      true_constant_ = LogicalConstant.create('true:t',
          self_.type_repository_.get_truth_value_type())
      false_constant_ = LogicalConstant.create('false:t',
          self_.type_repository_.get_truth_value_type())

      if len(self_.constants_files_) == 0:
        ontology_ = None
        if self_.ontology_closed_:
          raise RuntimeError(
              'Closed ontology requested, but no logical constants were provided.')
      else:
        constants_ = self_.read_constants_from_files(
            self_.constants_files_, self_.type_repository_)
        constants_.add(conjunction_predicate_)
        constants_.add(disjunction_predicate_)
        constants_.add(negation_predicate_)
        constants_.add(index_increase_predicate_)
        constants_.add(true_constant_)
        constants_.add(false_constant_)
        ontology_ = Ontology(constants_, self_.ontology_closed_)

      return LogicLanguageServices(self_.type_repository_,
          self_.numeral_type_name_,
          self_.type_comparator_,
          ontology_,
          conjunction_predicate_,
          disjunction_predicate_,
          negation_predicate_,
          index_increase_predicate_,
          true_constant_,
          false_constant_,
          self_.printer_)
