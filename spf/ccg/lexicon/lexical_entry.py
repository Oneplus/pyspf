#!/usr/bin/env python


class LexicalEntry(object):
    def __init__(self, tokens, category, origin):

        self.linked_entries = set()
        self.origin = None
        self.category = category
        self.tokens = tuple(tokens)
        # TODO
        self.hash_code_cache = self.calculate_hash_code()

    @staticmethod
    def parse(line, category_services, origin, text_filter=lambda x: x):
        """

        :param line:
        :param category_services:
        :type category_services:
        :param origin:
        :param text_filter:
        :return:
        """
        split = line.find(":-")
        if split > 0:
            tokens = text_filter(line[:split]).split()
            category = category_services.parse(line[split + 2:])
            return LexicalEntry(tokens, category, origin)
        else:
            raise RuntimeError("Unrecognized format for lexicon item: %s" % line)

    def add_linked_entries(self, entries):
        self.linked_entries.update(entries)

    def add_linked_entry(self, entry):
        self.linked_entries.add(entry)

    def clone_with_different_origin(self, new_origin):
        new_entry = LexicalEntry(self.tokens, self.category, new_origin)
        new_entry.add_linked_entries(self.linked_entries)
        return new_entry

    def __eq__(self, other):
        if not isinstance(other, LexicalEntry):
            return False
        if len(self.tokens) != len(other.tokens):
            return False
        return self.tokens == other.tokens and self.category == other.category

    def get_category(self):
        return self.category

    def get_origin(self):
        return self.origin

    def get_tokens(self):
        return self.tokens

    def has_words(self, words):
        return self.tokens == words

    def __hash__(self):
        return self.hash_code_cache

    def __str__(self):
        return "%s :- %s" % (" ".join(self.tokens), str(self.category))

    def calculate_hash_code(self):
        return (37 * 17 + hash(self.category)) * 37 + hash(self.tokens)

    class Origin(object):
        """ Mark for the origin of the lexicon entry """
        FIXED_DOMAIN = "fixed_domain"
        FIXED_LANG = "fixed_lang"
        HEURISTIC = "heuristic"
        LEARNED = "learned"
