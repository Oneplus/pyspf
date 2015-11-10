#!/usr/bin/env python

from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.language.type_.type_repository import TypeRepository
from spf.mr.lambda_.flexible_type_comparator import FlexibleTypeComparator
from spf.mr.lambda_.ccg.logical_expr_category_services import LogicalExpressionCategoryServices
import os


class TestServices(object):
    CATEGORY_SERVICES = LogicalExpressionCategoryServices(True, True)
    DEFAULT_TYPES_FILE = os.path.join(os.path.dirname(__file__), "resource-test", "geo.types")
    DEFAULT_ONTOLOGY_FILES = {os.path.join(os.path.dirname(__file__), "resource-test", "geo.consts.ont"),
                             os.path.join(os.path.dirname(__file__), "resource-test", "geo.preds.ont")}

    LogicLanguageServices.set_instance(LogicLanguageServices.Builder(TypeRepository(DEFAULT_TYPES_FILE), FlexibleTypeComparator())
                                       .close_ontology(False)
                                       .add_constants_to_ontology(DEFAULT_ONTOLOGY_FILES)
                                       .set_numeral_type_name("i").build())