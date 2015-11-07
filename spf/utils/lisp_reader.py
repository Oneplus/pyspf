#!/usr/bin/env python

class LispReader(object):
  '''
  Used to read data in lisp format. File leading with # will be escaped. Iteratively
  breaking lisp expression into sub sequences, like: 

    '(a (b c) (d e))' => ['a', '(b c)', '(d e)']
  '''

  def __init__(self_, handler):
    '''
    Parameter
    ---------
    handler: file object
    The handler to input file object.
    '''
    self_.handler_ = handler
    self_.lastc_ = ' '
    self_.skip_till_charater('(')
    self_.skip_white_space()

  def next(self_):
    '''
    Get next lisp element, can be a word or a nested list
    '''
    if self_.lastc_ == '(':
      return self_.read_list()
    return self_.read_word()

  def read_list(self_):
    result = '('
    depth = 1
    while depth != 0 and self_.lastc_ != '':
      self_.lastc_ = self_.handler_.read(1)
      if self_.lastc_ == '(': depth += 1
      if self_.lastc_ == ')': depth -= 1
      result += self_.lastc_
    self_.lastc_ = self_.handler_.read(1)
    self_.skip_white_space()
    return result

  def read_word(self_):
    result = ''
    while not self_.lastc_.isspace() and self_.lastc_ != ')' and self_.lastc_ != '':
      result += self_.lastc_
      self_.lastc_ = self_.handler_.read(1)
    self_.skip_white_space()
    return result

  def skip_till_charater(self_, seek):
    while self_.lastc_ != seek and self_.lastc_ != '':
      self_.lastc_ = self_.handler_.read(1)
    self_.lastc_ = self_.handler_.read(1)

  def skip_white_space(self_):
    while self_.lastc_.isspace() or self_.lastc_ == ')':
      self_.lastc_ = self_.handler_.read(1)

  def has_next(self_):
    return self_.lastc_ != ''


if __name__=='__main__':
  s = '(a b (c d) (e f))'
  from StringIO import StringIO
  reader = LispReader(StringIO(s))
  while reader.has_next():
    print reader.next()
