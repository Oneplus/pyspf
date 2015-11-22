#!/usr/bin/env python


class GraphParserI(object):
    def parse(self, pruning_filter, data_item, model, allow_word_skipping, temp_lexicon, beam_size):
        raise NotImplementedError("Need override")
