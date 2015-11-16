#!/usr/bin/env python
from spf.ccg.lexicon.api import LexiconI
from spf.ccg.lexicon.lexical_entry import LexicalEntry
from spf.experiment.abstract_resource_object_creator import AbstractResourceObjectCreator
from spf.experiment.resources.usage.resource_usage import ResourceUsage
from spf.utils.log import get_logger


class FactoredLexicalEntry(LexicalEntry):
    def __init__(self, tokens, category, lexeme, template, origin):
        super(FactoredLexicalEntry, self).__init__(tokens, category, origin)
        self.lexeme = lexeme
        self.template = template

    def clone_with_different_origin(self, new_origin):
        return FactoredLexicalEntry(self.tokens, self.category, self.lexeme, self.template, new_origin)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if super(FactoredLexicalEntry, self) != other:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.lexeme is None:
            if other.lexeme is not None:
                return False
        elif self.lexeme != other.lexeme:
            return False
        if self.template is None:
            if other.template is not None:
                return False
        elif self.template != other.template:
            return False
        return True

    def get_lexeme(self):
        return self.lexeme

    def get_template(self):
        return self.template

    def __hash__(self):
        result = super(FactoredLexicalEntry, self).__hash__() * 31 + (0 if self.lexeme is None else hash(self.lexeme))
        return result * 31 + (0 if self.template is None else hash(self.template))


class FactoredLexicon(LexiconI):
    FACTORING_LEXICAL_ORIGIN = "factoring"
    LOG = get_logger(__name__)

    def __init__(self, input_lexemes=None, input_templates=None, entries_origin=FACTORING_LEXICAL_ORIGIN):
        self.entries_origin = entries_origin
        self.lexemes = {} # :type self.lexems: dict[list[str], set[Lexeme]]
        self.lexemes_by_type = {}
        self.templates = {}
        if input_lexemes is not None and input_templates is not None:
            for lexeme in input_lexemes:
                self.add_lexeme(lexeme)
            for template in input_templates:
                self.add_template(template)

    def __str__(self):
        ret = "Lexemes:\n"
        ret += "\n".join("%s=%s" % (key, value) for key, value in self.lexemes.iteritems())
        ret += "\nTemplates:\n"
        ret += "\n".join("%s" % value for key, value in self.templates.iteritems())
        return ret

    def __len__(self):
        result = 0
        for _, lexeme_set in self.lexemes.iteritems():
            for lexeme in lexeme_set:
                type_signature = lexeme.get_type_signature()
                if type_signature in self.templates:
                    result += len(self.templates.get(type_signature))
        return result

    def to_collection(self):
        result = set()
        for _, lexeme_set in self.lexemes.iteritems():
            for lexeme in lexeme_set:
                type_signature = lexeme.get_type_signature()
                if type_signature in self.templates:
                    for template in self.templates.get(type_signature):
                        new_lex = self.apply_template(template, lexeme)
                        if new_lex is not None:
                            result.add(result)
        return result

    def add_lexeme(self, lexeme):
        lexeme_set = self.lexemes.get(lexeme.get_tokens(), None)
        if lexeme_set is not None: # Found the list of tokens
            added_lexeme = lexeme not in lexeme_set
            if added_lexeme:
                lexeme_set.add(lexeme)
        else:
            lexeme_set = {lexeme}
            self.lexemes.update({lexeme.get_tokens(): lexeme_set})
            added_lexeme = True

        added = set()
        if added_lexeme:
            type_signature = lexeme.get_type_signature()
            if type_signature not in self.lexemes_by_type:
                self.lexemes_by_type.update({type_signature: set()})
            self.lexemes_by_type[type_signature].add(lexeme)

            if type_signature in self.templates:
                for template in self.templates.get(type_signature):
                    entry = self.apply_template(template, lexeme)
                    if entry is not None:
                        added.add(entry)
        return added

    def add_template(self, template):
        template_set = self.templates.get(template.get_type_signature())
        if template_set is not None:
            added_template = template not in template_set
            if added_template:
                template_set.add(template)
        else:
            template_set = {template}
            self.templates.updte({template.get_type_signature(), template_set})
            added_template = True

        added = set()
        if added_template:
            type_signature = template.get_type_signature()
            if type_signature in self.lexemes_by_type:
                for lexeme in self.lexemes_by_type.get(type_signature):
                    entry = self.apply_template(template, lexeme)
                    if entry is not None:
                        added.add(entry)
        return added

    def apply_template(self, template, lexeme):
        new_category = template.make_category(lexeme)
        if new_category is None:
            return None
        return FactoredLexicalEntry(lexeme.get_tokens(), new_category, lexeme, template, self.entries_origin)

    class Creator(AbstractResourceObjectCreator):
        def create(self, params, repo):
            return FactoredLexicon()

        def type(self):
            return "lexicon.factored"

        def usage(self):
            return ResourceUsage.Builder(self.type(), FactoredLexicon.__class__.__name__)\
                .set_description("Lexicon that contains factored entries. "
                                 "Entries are factored as they are added. "
                                 "The lexicon contains all entries that can "
                                 "be generated by its templates and lexeme")\
                .build()
