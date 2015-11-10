#!/usr/bin/env python
from spf.experiment.resources.usage.param_usage import ParamUsage


class ResourceUsage(object):
    """ The class for resource usage description """
    def __init__(self, resource_name, resource_class, description, param_usages):
        """
        :type resource_name: str
        :type resource_class: str
        :type description: str
        :type param_usages: list[ParamUsage]
        :return:
        """
        self.resource_name = resource_name
        self.resource_class = resource_class
        self.description = description
        self.param_usages = param_usages

    class Builder(object):
        def __init__(self, resource_name, resource_class):
            """
            :type resource_name: str
            :type resource_class: str
            :return:
            """
            self.resource_name = resource_name
            self.resource_class = resource_class
            self.resource_description = None
            self.param_usages = []

        def add_param(self, *args):
            if len(args) == 1 and isinstance(args[0], ParamUsage):
                self.param_usages.append(args[0])
            elif len(args) == 3:
                if isinstance(args[1], str):
                    self.param_usages.append(ParamUsage(args[0], args[1], args[2]))
                else:
                    self.param_usages.append(ParamUsage(args[0], args[1].__class__.__name__, args[2]))
            return self

        def build(self):
            return ResourceUsage(self.resource_name, self.resource_class, self.resource_description, self.param_usages)

        def set_description(self, description):
            self.resource_description = description
            return self
