#!/usr/bin/env python


class ResourceCreatorRepository(object):
    def __init__(self):
        self.creators = {}

    def get_creators(self, name):
        return self.creators.get(name, None)

    def register_resource_creator(self, creator):
        self.creators.update({creator.type(): creator})
