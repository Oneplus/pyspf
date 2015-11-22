#!/usr/bin/env python


class SpanI(object):
    def __init__(self):
        self.externally_pruned = False

    def add_to_exisiting(self, existing_cell, new_cell):
        raise NotImplementedError("Override")

    def get(self, cell):
        raise NotImplementedError("Override")

    def is_pruned(self):
        raise NotImplementedError("Override")

    def min_non_lexical_score(self):
        raise NotImplementedError("Override")

    def offer(self, cell):
        """

        :param Cell cell:
        :return bool:
        """