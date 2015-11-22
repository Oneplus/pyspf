#!/usr/bin/env python
from spf.parser.graph.api import GraphParserI
from spf.utils.log import get_logger


class CKYParserI(GraphParserI):
    LOG = get_logger(__name__)

    def __init__(self, beam_size, binary_rules, sentence_lexicon_generators,
                 word_skipping_lexical_generator, category_services, prune_lexical_cells,
                 complete_parse_filter,
                 unary_rules,
                 category_transformation):
        """

        :param int beam_size:
        :param list[CKYBinaryParsingRule] binary_rules:
        :param list[SentenceLexiconGenerator] sentence_lexicon_generators:
        :param word_skipping_lexical_generator:
        :param category_services:
        :param prune_lexical_cells:
        :param complete_parse_filter:
        :param list[CKYUnaryParsingRule] unary_rules:
        :param functor category_transformation:
        :return:
        """
        self.beam_size = beam_size
        self.binary_rules = binary_rules
        self.sentence_lexicon_generators = sentence_lexicon_generators
        self.word_skipping_lexical_generator = word_skipping_lexical_generator
        self.category_services = category_services
        self.complete_parse_filter = complete_parse_filter
        self.unary_rules = unary_rules
        self.category_transformation = category_transformation
        self.LOG.info("Init :: %s : binary rules=%s" % (__name__, binary_rules))
        self.LOG.info("Init :: %s : unary rules=%s" % (__name__, unary_rules))

    def is_complete_span(self, start, end, sentence_length):
        return start == 0 and end == sentence_length - 1

    def is_full_parse(self, start, end, category, sentence_length):
        return self.is_complete_span(start, end, sentence_length) and self.complete_parse_filter.is_valid(category)

    def process_split(self, start, end, split, sentence_length, chart, cell_factory, pruning_filter, model):
        """

        :param int start:
        :param int end:
        :param int split:
        :param int sentence_length:
        :param Chart chart:
        :param AbstractCellFactory cell_factory:
        :param FilterI pruning_filter:
        :param DataItemModelI model:
        :return:
        """
        self.LOG.debug("Processing split (%d, %d)[%d] with %d x %d cells", start, end, split,
                       chart.span_size(start, start + split),
                       chart.span_size(start + split + 1, end))