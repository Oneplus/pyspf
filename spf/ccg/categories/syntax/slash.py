#!/usr/bin/env python

class _Slash(object):
  def __init__(self_, c):
    self_.c = c

  def __hash__(self_):
    return 31 + ord(self_.c)

  def __eq__(self_, other):
    return id(self_) == id(other)

  def __str__(self_):
    return self_.c

  def get_char(self_):
    return self_.c

class Slash(object):
  BACKWARD = _Slash('\\')
  FOWARD   = _Slash('/')
  VERTICAL = _Slash('|')

  @staticmethod
  def get_slash(c):
    if c == Slash.BACKWARD.get_char():
      return Slash.BACKWARD
    elif c == Slash.FOWARD.get_char():
      return Slash.FOWARD
    elif c == Slash.VERTICAL.get_char():
      return Slash.VERTICAL
    else:
      return None
