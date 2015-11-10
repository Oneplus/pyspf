#!/usr/bin/env python
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.parameterized_experiment import ParameterizedExperiment
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.parser.ccg.rules.binary_rule_set import BinaryRuleSet
from spf.parser.ccg.rules.primitivebinary.application import BackwardApplication, ForwardApplication


class ApplicationCreator(AbstractResourceObjectCreator):
    def __init__(self, type_="rule.application"):
        self.type_ = type_

    def create(self, params, repo):
        rules = [ForwardApplication(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE)),
                 BackwardApplication(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE))]
        return BinaryRuleSet(rules)

    def type(self):
        return self.type_

    def usage(self):
        return ResourceUsage.Builder(self.type_, AbstractResourceObjectCreator.__class__.__name__).build()

