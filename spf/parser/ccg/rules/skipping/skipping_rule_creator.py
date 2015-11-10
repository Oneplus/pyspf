#!/usr/bin/env python
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.parameterized_experiment import ParameterizedExperiment
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.parser.ccg.rules.skipping.api import AbstractSkippingRule
from spf.parser.ccg.rules.skipping.skipping_rule import BackwardSkippingRule, ForwardSkippingRule


class SkippingRuleCreator(AbstractResourceObjectCreator):
    def __init__(self, type_="rule.skipping"):
        self.type_ = type_

    def create(self, params, repo):
        return [ForwardSkippingRule(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE)),
                BackwardSkippingRule(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE))]

    def type(self):
        return self.type_

    def usage(self):
        return ResourceUsage.Builder(self.type_, AbstractSkippingRule.__class__.__name__).build()
