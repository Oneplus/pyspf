#!/usr/bin/env python


class Type(object):
    """ The basic abstract object for type """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self == other

    def __neq__(self, other):
        return not self.__eq__(other)

    def get_name(self):
        return self.name

    def hash_code(self):
        return self.hash_code_cache

    def is_array(self):
        raise NotImplementedError()

    def is_complex(self):
        raise NotImplementedError()

    def is_extending(self, other):
        raise NotImplementedError()

    def is_extending_or_extended_by(self, other):
        """
        For hierachical type ontology
        :param other:
        """
        raise NotImplementedError()

    def __str__(self):
        return ''

    def __hash__(self):
        return hash(self.name)

        # def read_resolve(self):
        #  ''' querying the type repository and get the equivalent class '''
        #  return LogicalLanguageServices.get_type_repository().get_type_create_if_needed(self.name)
