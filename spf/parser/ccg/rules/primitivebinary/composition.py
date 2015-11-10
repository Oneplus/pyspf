#!/usr/bin/env python
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.parser.ccg.rules.primitivebinary.api import AbstractComposition
from spf.experiment.parameterized_experiment import ParameterizedExperiment
from spf.parser.ccg.rules.rule_name import Direction


class ForwardComposition(AbstractComposition):
    def __init__(self, category_services, order):
        super(ForwardComposition, self).__init__(self.RULE_LABEL, Direction.BACKWARD, order, category_services)

    def apply(self, left, right):
        self.do_composition(left, right, False)

    class Creator(AbstractResourceObjectCreator):
        def __init__(self, type_="rule.composition.forward"):
            self.type_ = type_

        def create(self, params, repo):
            # TODO: params.get, try optparse
            return ForwardComposition(repo, ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE, params.get)

        def type(self):
            return self.type_

        def usage(self):
            return ResourceUsage.Builder(self.type_, ForwardComposition.__class__.__name__)\
                .add_param("eisner_normal_form", "boolean",
                           "Use Eisner normal form for composition (default: false)")\
                .add_param("order", int.__class__.__name__,
                           "Composition order (for English, around 3 should be the max, default 0)")\
                .build()


class BackwardComposition(AbstractComposition):
    def __init__(self, category_services, order):
        super(BackwardComposition, self).__init__(category_services, order)

    def apply(self, left, right):
        return self.do_composition(left, right, True)

    class Creator(AbstractResourceObjectCreator):
        def __init__(self, type_="rule.composition.backward"):
            self.type_ = type_

        def create(self, params, repo):
            # TODO: params.get, try optparse
            return BackwardComposition(repo, ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE, params.get)

        def type(self):
            return self.type_

        def usage(self):
            return ResourceUsage.Builder(self.type_, BackwardComposition.__class__.__name__)\
                .add_param("eisner_normal_form", "boolea",
                           "Use Eisner normal form for composition (default: false)")\
                .add_param("order", int.__class__.__name__,
                           "Composition order (for English, around 3 should be the max, default 0)")\
                .build()
