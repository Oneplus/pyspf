#!/usr/bin/env python
import re


class ParameterizedExperiment(object):
    CATEGORY_SERVICES_RESOURCE = "category_services"
    DOMAIN_ONTOLOGY_RESOURCE = "domain_ontology"
    EXECUTOR_RESOURCE = "executor"
    ONTOLOGY_RESOURCE = "ontology"
    PARSER_RESOURCE = "parser"
    INCLUDE_DIRECTIVE = "include"
    COMMENT_REGEX = re.compile("\\s*//")

    def __init__(self, filename, env_params, creator_repo, root_dir):
        """
        The initializer for ParameterizedExperiment
        :param env_params:
        :param creator_repo:
        :param root_dir:
        :return:
        """
        self.creator_repo = creator_repo
        self.root_dir = root_dir

        n_lines = 0
        try:
            mutable_parameters = {}
            for line in open(filename, 'r'):
                n_lines += 1
                line = self.escape(line)
                if len(line) == 0:
                    continue

                split = line.strip().split("=", 2)
                if split[0] == self.INCLUDE_DIRECTIVE:
                    mutable_parameters.update(self.read_include_parameters(split[1]))
                else:
                    mutable_parameters.update({split[0]: split[1]})

            self.global_params = {}
            for key, value in mutable_parameters.iteritems():
                self.global_params.update({key, value})


        except Exception, e:
            raise Exception(e, "error occured at: %d" % n_lines)

    @classmethod
    def read_include_parameters(cls, filename):
        try:
            ret = {}
            for line in open(filename, 'r'):
                split = line.strip().split("=", 2)
                ret.update({split[0]: split[1]})
            return ret
        except Exception, e:
            pass

    @classmethod
    def escape(cls, line):
        line = line.strip()
        if line.startswith("#"):
           return ""
        line = cls.COMMENT_REGEX.split(line)[0]
        return line