#!/usr/bin/env python

from spf.mr.lambda_.logical_expr import LogicalExpressionComparator


class StrictTypeComparator(LogicalExpressionComparator):
    def verify_arg_type(self, signature_type, arg_type):
        return arg_type.is_extending(signature_type)
