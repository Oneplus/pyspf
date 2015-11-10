#!/usr/bin/env python


class StrictTypeComparator(object):
    def verify_arg_type(self, signature_type, arg_type):
        return arg_type.is_extending(signature_type)
