#!/usr/bin/env python


class ParamUsage(object):
    """ The very basic type for Parameter Usage. """
    def __init__(self, name, value_type, description):
        """

        :param name: str
        :param value_type: str
        :param description: str
        :return:
        """
        self.name = name
        self.value_type = value_type
        self.description = description

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_value_type(self):
        return self.value_type

    def __str__(self):
        return "%s [%s] %s" % (self.name, self.value_type, self.description)