#!/usr/bin/env python


class SlashToken(object):
    def __init__(self, c):
        self.c = c  # The character

    def __hash__(self):
        return 31 + ord(self.c)

    def __eq__(self, other):
        return id(self) == id(other)

    def __str__(self):
        return self.c

    def get_char(self):
        return self.c


class Slash(object):
    BACKWARD = SlashToken('\\')
    FORWARD = SlashToken('/')
    VERTICAL = SlashToken('|')

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
