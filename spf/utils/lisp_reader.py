#!/usr/bin/env python


class LispReader(object):
    """
    Used to read data in lisp format. File leading with # will be escaped. Iteratively
    breaking lisp expression into sub sequences, like:

    '(a (b c) (d e))' => ['a', '(b c)', '(d e)']
    """

    def __init__(self, handler):
        self.handler = handler
        self.lastc = ' '
        self.skip_till_charater('(')
        self.skip_white_space()

    def next(self):
        """ Get next lisp element, can be a word or a nested list """
        if self.lastc == '(':
            return self.read_list()
        return self.read_word()

    def read_list(self):
        result = '('
        depth = 1
        while depth != 0 and self.lastc != '':
            self.lastc = self.handler.read(1)
            if self.lastc == '(':
                depth += 1
            if self.lastc == ')':
                depth -= 1
            result += self.lastc
        self.lastc = self.handler.read(1)
        self.skip_white_space()
        return result

    def read_word(self):
        result = ''
        while not self.lastc.isspace() and self.lastc != ')' and self.lastc != '':
            result += self.lastc
            self.lastc = self.handler.read(1)
        self.skip_white_space()
        return result

    def skip_till_charater(self, seek):
        while self.lastc != seek and self.lastc != '':
            self.lastc = self.handler.read(1)
        self.lastc = self.handler.read(1)

    def skip_white_space(self):
        while self.lastc.isspace() or self.lastc == ')':
            self.lastc = self.handler.read(1)

    def has_next(self):
        return self.lastc != ''
