#!/usr/bin/env python


class MultiCKYParser(object):

    class Builder(object):
        def __init__(self, category_services, complete_parse_filter):
            """

            :param CategoryService category_services:
            :param Function complete_parse_filter: The filter for complete parse, like checking whether it Syntax
                                                    category is S
            :return:
            """
            self.category_services = category_services
            self.complete_parse_filter = complete_parse_filter
            # TODO
            self.word_skipping_lexical_generator = SimpleWordSkippingLexicalGenerator(category_services)
            self.binary_rules = []
            self.unary_rules = []
            self.sentence_lexical_generator = []
            self.pre_chart_pruning = False
            self.prune_lexical_cells = False
            self.max_number_of_cells_in_span = 50
            self.category_transformation = None

        def add_parse_rule(self, rule):
            # TODO CKYUnaryParsingRule
            if isinstance(rule, CKYUnaryParsingRule):
                self.unary_rules.append(rule)
            elif isinstance(rule, CKYBinaryParsingRule):
                self.binary_rules.append(rule)
            else:
                raise RuntimeError("Wrong type for argument")
            return self

        def set_category_transformation(self, category_transformation):
            self.category_transformation = category_transformation
            return self

        def set_word_skipping_generator(self, word_skipping_generator):
            self.word_skipping_lexical_generator = word_skipping_generator
            return self

        def build(self):
            return MultiCKYParser()