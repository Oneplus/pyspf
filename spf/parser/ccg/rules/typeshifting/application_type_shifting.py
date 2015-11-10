#!/usr/bin/env python
from spf.ccg.categories.complex_category import ComplexCategory
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.parameterized_experiment import ParameterizedExperiment
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.parser.ccg.rules.api import UnaryParseRuleI
from spf.parser.ccg.rules.parse_rule_result import ParseRuleResult
from spf.parser.ccg.rules.rule_name import RuleName


class ApplicationTypeShifting(UnaryParseRuleI):
    def __init__(self, label, function, category_services):
        self.rule_name = RuleName.create(label)
        self.function = function
        self.category_services = category_services
        self.input_syntax = function.get_syntax().get_right()

    def apply(self, category):
        shifted = self.category_services.apply(self.function, category)
        if shifted is None:
            return []
        else:
            return [ParseRuleResult(self.rule_name, shifted)]

    def get_name(self):
        return self.rule_name

    def __str__(self):
        return str(self.rule_name)

    def is_valid_argument(self, category):
        return category.get_syntax() == self.input_syntax

    class Creator(AbstractResourceObjectCreator):
        def __init__(self, type_="rule.shifting.generic.application"):
            self.type_ = type_

        def create(self, params, repo):
            category_services = repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE)
            return ApplicationTypeShifting(
                params.get("name"),
                category_services.parse(params.get("function"), category_services)
            )

        def type(self):
            return self.type_

        def usage(self):
            return ResourceUsage.Builder(self.typ_, ApplicationTypeShifting.__class__.__name__)\
                .add_param("name", str.__class__, "Rule name")\
                .add_param("function", ComplexCategory.__class__, "Function category")\
                .build()