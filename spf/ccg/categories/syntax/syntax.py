#!/usr/bin/env python

class AbstractSyntax(object):
  ''' Define interface for Syntax '''
  def __hash__(self_):
    raise NotImplementedError()

  def __str__(self_):
    raise NotImplementedError()

  def num_slashes(self_):
    raise NotImplementedError()


class SimpleSyntax(AbstractSyntax):
  def __init__(self_, label_):
    self_.label_ = label_
    self_.hash_code_ = self_.calculate_hash_code()

  def __eq__(self_, other):
    if id(self_) == id(other):
      return True
    if other is None:
      return False
    if not isinstance(other, SimpleSyntax):
      return False
    if self_.label_ is None:
      if other.label_ is not None:
        return False
    elif label_ != other.label_:
      return False
    return True

  def __hash__(self_):
    return self_.hash_code_

  def __str__(self_):
    return self_.label_

  def num_slashes(self_):
    return 0

  def calculate_hash_code(self_):
    return 31 + 0 if self_.label_ is None else hash(self_.label_)


class Syntax(object):
  ADJ = SimpleSyntax('ADJ')
  AP  = SimpleSyntax('AP')
  C   = SimpleSyntax('C')
  DEG = SimpleSyntax('DEG')

  EMPTY = SimpleSyntax('EMPTY')

  N  = SimpleSyntax('N')
  NP = SimpleSyntax('NP')
  PP = SimpleSyntax('PP')
  S  = SimpleSyntax('S')

  STRING_MAPPING = {
      'ADJ':   ADJ,
      'AP':    AP,
      'C':     C,
      'DEG':   DEG,
      'EMPTY': EMPTY,
      'N':     N,
      'NP':    NP,
      'PP':    PP,
      'S':     S
      }

  VALUES = set(STRING_MAPPING.values())
