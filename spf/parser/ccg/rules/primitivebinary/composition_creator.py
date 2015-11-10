#!/usr/bin/env python
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.parameterized_experiment import ParameterizedExperiment
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.parser.ccg.rules.binary_rule_set import BinaryRuleSet
from spf.parser.ccg.rules.primitivebinary.api import AbstractComposition
from spf.parser.ccg.rules.primitivebinary.composition import BackwardComposition, ForwardComposition


class CompositionCreator(AbstractResourceObjectCreator):
    def __init__(self, type_="rule.composition"):
        self.type_ = type_

    def create(self, params, repo):
        max_order = params.max_order
        crossing = params.crossing
        rules = []
        while max_order >= 0:
            rules.extend([
                ForwardComposition(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE), max_order),
                BackwardComposition(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE), max_order)])
            max_order -= 1

        return BinaryRuleSet(rules)

    def type(self):
        return self.type_

    def usage(self):
        return ResourceUsage.Builder(self.type_, AbstractComposition.__class__.__name__).build()
