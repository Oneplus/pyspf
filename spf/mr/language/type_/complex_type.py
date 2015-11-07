#!/usr/bin/env python

from spf.mr.language.type_.type_ import Type

class ComplexType(Type):
  COMPLEX_TYPE_CLOSE_PAREN = '>'
  COMPLEX_TYPE_OPEN_PAREN = '<'
  COMPLEX_TYPE_SEP = ','

  def __init__(self_, label, domain_, range_):
    super(ComplexType, self_).__init__(label)
    self_.domain_ = domain_
    self_.range_ = range_

  @staticmethod
  def composeString(range_, domain_, option):
    ret = '<{domain}{option},{range}>'.format(
        domain=str(domain_),
        option=('' if option is None else str(option)),
        range=str(range_))
    return ret

  @staticmethod
  def create(string_, domain_, range_, option):
    if option is None:
      return ComplexType(string_, domain_, range_)
    else:
      raise NotImplementedError('create RecursiveComplexType is not implemented')

  def get_domain(self_):
    return self_.domain_

  def get_range(self_):
    return self_.range_

  def is_array(self_):
    return False

  def is_complex(self_):
    return True

  def is_extending(self_, other):
    ''' Whether a class is extending other depends on its range and its domain, if
    both its range and its domain are extending other, it should be extending other.
    '''
    return (other is not None and
        (self_ == other or (self_.domain_.is_extending(other.get_domain()) and
          self_.range_.is_extending(other.get_range()))))

  def is_extending_or_extended_by(self_, other):
    return self_.is_extending(other) or other.is_extending(self_)

  def is_order_sensitive(self_):
    return True

  def __str__(self_):
    return self_.get_name()
