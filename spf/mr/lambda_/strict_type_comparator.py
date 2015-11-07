#!/usr/bin/env python

class StrictTypeComparator(object):
  def verify_arg_type(self_, signature_type_, arg_type_):
    return arg_type_.is_extending(signature_type_)
