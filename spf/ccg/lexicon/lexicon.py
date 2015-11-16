#!/usr/bin/env python
from spf.ccg.lexicon.api import LexiconI
from spf.ccg.lexicon.lexical_entry import LexicalEntry
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.resources.usage.resource_usage import ResourceUsage


class Lexicon(LexiconI):
    SAVED_LEXICON_ORIGIN = "saved"

    def __init__(self, lexicon=None):
        self.entries = set()
        self.empty_set = set()
        if lexicon is not None and isinstance(lexicon, LexiconI):
            self.entries.update(lexicon.to_collection())

    def copy(self):
        # TODO
        pass

    def add(self, lex):
        if lex in self.entries:
            return None
        else:
            self.entries.add(lex)
            return lex

    def update(self, entries):
        added = set()
        for entry in entries:
            if entry not in self.entries:
                added.add(entry)
                self.entries.add(entry)
        return added

    def add_entries_from_file(self, filename, text_filter, category_service, origin):
        try:
            added = set()
            line_count = 0
            try:
                for line in open(filename, "r"):
                    line_count += 1
                    line = line.strip()
                    if len(line) != 0 and not line.startswith("//"):
                        added.add(self.add(LexicalEntry.parse(line, category_service, origin, text_filter)))
            except Exception, e:
                raise RuntimeError("Reading input file %s failed at %d" % (filename, line_count), e)
            return added
        except Exception, e:
            raise Exception(e)

    def contains(self, lex):
        return lex in self.entries

    def get_lex_entries(self, words):
        matched_entries = []
        for entry in self.entries:
            if entry.has_words(words):
                matched_entries.append(entry)
        return matched_entries

    def retain_all(self, entries_to_keep):
        self.entries = set(entries_to_keep)
        return self.entries

    def __len__(self):
        return self.entries.__len__()

    def to_collection(self):
        return self.entries

    def __str__(self):
        return "\n".join(str(entry) for entry in self.entries)

    class Creator(AbstractResourceObjectCreator):
        def create(self, params, repo):
            return Lexicon()

        def type(self):
            return "lexicon"

        def usage(self):
            return ResourceUsage.Builder(self.type(), Lexicon.__class__.__name__)\
                .set_description("A simple collection of lexical entries").build()
