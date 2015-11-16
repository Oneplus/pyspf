#!/usr/bin/env python


class LexiconI(object):
    def get_lex_entries(self, words):
        raise NotImplementedError()

    def contains(self, lex):
        raise NotImplementedError()

    def copy(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def to_collection(self):
        raise NotImplementedError()

    def add(self, lex):
        raise NotImplementedError()

    def update(self, entries):
        """
        Equivalent to addAll
        :param entries:
        :return:
        """
        raise NotImplementedError()

    def add_entries_from_file(self, filename, text_filter, category_service, origin):
        raise NotImplementedError()

    def retain_all(self, entries):
        raise NotImplementedError()
