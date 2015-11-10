#!/usr/bin/env python
import sys
import os
from spf.ccg.lexicon.factored.lambda_.factored_lexicon_services import FactoredLexiconServices
from spf.mr.lambda_.ccg.logical_expr_category_services import LogicalExpressionCategoryServices
from spf.mr.lambda_.flexible_type_comparator import FlexibleTypeComparator
from spf.mr.lambda_.logic_language_services import LogicLanguageServices
from spf.mr.lambda_.logical_const import LogicalConstant
from spf.mr.language.type_.type_repository import TypeRepository
from spf.utils.log import get_logger

LOG = get_logger(__name__)


def main(args=["E:\\workspace\\spf\\geoquery"]):
    resource_dir = os.path.join(args[0], "resources/")
    experiments_dir = os.path.join(args[0], "experiments/")
    data_dir = os.path.join(experiments_dir, "data")

    types_files = os.path.join(resource_dir, "geo.types")
    predicate_ontology = os.path.join(resource_dir, "geo.preds.ont")
    simple_ontology = os.path.join(resource_dir, "geo.consts.ont")

    LogicLanguageServices.set_instance(
        LogicLanguageServices.Builder(TypeRepository(types_files), FlexibleTypeComparator())
            .add_constants_to_ontology(simple_ontology)
            .add_constants_to_ontology(predicate_ontology)
            .set_numeral_type_name("i")
            .close_ontology(True)
            .build()
    )

    category_services = LogicalExpressionCategoryServices(True, True)
    unfactored_constants = {LogicalConstant.read("the:<<e,t>,e>"), LogicalConstant.read("exists:<<e,t>,t>")}

    FactoredLexiconServices.set(unfactored_constants)


if __name__ == "__main__":
    main()
