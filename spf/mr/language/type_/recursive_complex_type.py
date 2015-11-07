#!/usr/bin/env python

import re
from spf.mr.language.type_.complex_type import ComplexType

class Option(object):
  DOMAIN_REPEAT_ORDER_INSENSITIVE = '*'
  DOMAIN_REPEAT_ORDER_SENSITIVE = '+'
  STRING_PATTERN = re.compile("(?P<type>.+?)(((?P<order>[*+])((?P<minargs>\\d+)|()))|())$")

  def __init__(self_, order_sensitive_, min_args_):
    self_.order_sensitive_ = order_sensitive_
    self_.min_args_ = min_args_

  @staticmethod
  def parse(string_):
    ''' parse string like t*10 '''
    m = Option.STRING_PATTERN.match(string_)
    if m is not None:
      type_ = m.group('type')
      if m.group('order') is not None:
        order_sensitive_ = True if m.group('order') == '+' else False
        min_args_ = 2 if m.group('minargs') is None else int(m.group('minargs'))
        return (type_, Option(order_sensitive_, min_args_))
      else:
        return (type_, None)
    else:
      raise 'Invalid type string'


class RecursiveComplexType(ComplexType):
  ''' RecursiveComplexType is used to handle the type like <t*,t> '''
  MIN_NUM_ARGUMENT = 2

  def __init__(self_, domain_, range_, *args):
    self_.domain_ = domain_
    self_.range_ = range_
    if len(args) == 2:
      self_.order_sensitive_ = args[0]
      self_.min_args_ = args[1]
    elif len(args) == 1:
      self_.order_sensitive_ = args[0].order_sensitive_
      self_.min_args_ = args[0].min_args_

  def get_final_range(self_):
    return super(RecursiveComplexType, self_).get_range()

  def get_min_args(self_):
    return self_.min_args_

  def get_range(self_):
    # TODO understanding this.
    return self_

  def get_option(self_):
    return Option(self_.order_sensitive_, self_.min_args_)

  def is_extending(self_, other):
    return (other is not None and
        (other == self_ or (isinstance(other, RecursiveComplexType) and
          (self_.min_args_ == other.min_args_) and
          (self_.order_sensitive_ == other.order_sensitive_) and
          (self_.get_domain().is_extending(other.get_domain())) and
          (self_.get_final_range().is_extending(other.get_final_range())))
          ))

  def is_order_sensitive(self_):
    return self_.order_sensitive_

  def __str__(self_):
    return self_.get_name()
