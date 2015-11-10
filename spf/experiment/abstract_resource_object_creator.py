#!/usr/bin/env python


class AbstractResourceObjectCreator(object):
    def create(self, params, repo):
        raise NotImplementedError()

    def type(self):
        raise NotImplementedError()

    def usage(self):
        raise NotImplementedError()