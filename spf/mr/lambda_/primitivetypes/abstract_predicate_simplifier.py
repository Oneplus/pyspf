#!/usr/bin/env python


class AbstractPredicateSimplifier(object):
    def simplify(self, expr):
        raise NotImplementedError()