#!/usr/bin/env python
from spf.ccg.categories.complex_category import ComplexCategory
from spf.ccg.categories.syntax.slash import Slash
from spf.parser.ccg.rules.api import BinaryParseRuleI
from spf.parser.ccg.rules.parse_rule_result import ParseRuleResult
from spf.parser.ccg.rules.rule_name import RuleName
from spf.utils.log import get_logger


class AbstractApplication(BinaryParseRuleI):
    RULE_LABEL = "apply"

    def __init__(self, label, direction, category_services):
        self.name = RuleName.create(label, direction)
        self.category_services = category_services

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False

        if self.category_services is None:
            if other.category_services is not None:
                return False
        elif self.category_services != other.category_services:
            return False

        if self.name is None:
            if other.name is not None:
                return False
        elif self.name != other.name:
            return False
        return True

    def get_name(self):
        return self.name

    def __hash__(self):
        result = 31 + (0 if self.category_services is None else hash(self.category_services))
        result = 31 * result + (0 if self.name is None else hash(self.name))
        return result

    def __str__(self):
        return str(self.name)

    def do_application(self, function, argument, backward):
        if isinstance(function, ComplexCategory):
            if function.get_slash() == (Slash.BACKWARD if backward else Slash.FORWARD):
                result = self.category_services.apply(function, argument)
                if result is not None:
                    return [ParseRuleResult(self.name, result)]
        return []


class AbstractComposition(BinaryParseRuleI):
    LOG = get_logger(__name__)
    RULE_LABEL = "comp"

    def __init__(self, label, direction, order, category_services):
        self.order = order
        self.name = RuleName.create(label, direction, order)
        self.category_services = category_services

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        if self.category_services is None:
            if other.category_services is not None:
                return False
        elif self.category_services != other.category_services:
            return False

        if self.name is None:
            if other.name is not None:
                return False
        elif self.name != other.name:
            return False
        return True

    def get_name(self):
        return self.name

    def __hash__(self):
        result = 31 + (0 if self.category_services is None else hash(self.category_services))
        result = result * 31 + (0 if self.name is None else hash(self.name))
        return result

    def __str__(self):
        return self.name

    def do_composition(self, primary, secondary, backward):
        self.LOG.debug("applying %s, primary=%s, secondary=%s" % (self.name, primary, secondary))
        if isinstance(primary, ComplexCategory) and isinstance(secondary, ComplexCategory):
            if primary.get_slash() != (Slash.BACKWARD if backward else Slash.FORWARD):
               return []
            result = self.category_services.compose(primary, secondary, self.order)
            if result is not None:
                return ParseRuleResult(self.name, result)
        return []
