#!/usr/bin/env python
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.parameterized_experiment import ParameterizedExperiment
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.mr.lambda_.ccg.logical_expr_category_services import AbstractCategoryServices
from spf.parser.ccg.rules.primitivebinary.api import AbstractApplication
from spf.parser.ccg.rules.rule_name import Direction


# The Forward application rule.
class ForwardApplication(AbstractApplication):
    def __init__(self, category_services):
        """
        :type category_services: AbstractCategoryServices
        :return:
        """
        super(ForwardApplication, self).__init__(AbstractApplication.RULE_LABEL, Direction.FORWARD, category_services)

    def apply(self, left, right):
        """

        :type left:
        :type right:
        :return:
        """
        self.do_application(left, right,False)

    class Creator(AbstractResourceObjectCreator):
        def __init__(self, type_="rule.application.forward"):
            self.type_ = type_

        def create(self, params, repo):
            return ForwardApplication(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE))

        def type(self):
            return self.type_

        def usage(self):
            return ResourceUsage.Builder(self.type_, ForwardApplication.__class__.__name__).build()


# The Backward Application Rule
class BackwardApplication(AbstractApplication):
    def __init__(self, category_services):
        super(BackwardApplication, self).__init__(AbstractApplication.RULE_LABEL, Direction.BACKWARD, category_services)

    def apply(self, left, right):
        self.do_application(left, right, False)

    class Creator(AbstractResourceObjectCreator):
        def __init__(self, type_="rule.application.backward"):
            self.type_ = type_

        def create(self, params, repo):
            return BackwardApplication(repo.get_resource(ParameterizedExperiment.CATEGORY_SERVICES_RESOURCE))

        def type(self):
            return self.type_

        def usage(self):
            return ResourceUsage.Builder(self.type_, BackwardApplication.__class__.__name__).build()