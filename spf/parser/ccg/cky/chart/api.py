#!/usr/bin/env python


class CKYParseStepI(object):
    """ A temporary class for storing the parsing step """
    def __init__(self, root, left_child, right_child, is_full_parse, rule_name, model):
        """

        :param Category root:
        :param Cell left_child:
        :param Cell right_child:
        :param bool is_full_parse:
        :param RuleName rule_name:
        :param DataItemModel model:
        :return:
        """
        self.root = root
        self.is_full_parse = is_full_parse
        self.is_unary = (right_child is None)
        if left_child is not None:
            if self.is_unary:
                self.children = (left_child, )
            else:
                self.children = (left_child, right_child)
        else:
            self.children = tuple()
        self.rule_name = rule_name
        self.lexical_entry = None
        self.local_features = model.compute_features(self)
        self.local_score = model.score(self)

    def clone_with_unary(self, unary_rule_result, model, full_parse_after_unary):
        """

        :param unary_rule_result:
        :param model:
        :param full_parse_after_unary:
        :return:
        """
        raise NotImplementedError("Override")

    def get_child(self, index):
        return self.get_child_cell(index)

    def get_child_cell(self, index):
        return self.children[index]

    def get_local_features(self):
        return self.local_features

    def get_local_score(self):
        return self.local_score

    def num_children(self):
        return len(self.children)

    def __str__(self):
        return self.to_string(True)

    def to_string(self, recursive):
        """

        :param bool recursive:
        :return:
        """
        ret = "[%s] :: " % self.rule_name
        for child in self.children:
            if recursive:
                ret += str(child)
            else:
                ret += str(hash(child))
            ret += ", "
        ret += " :: localFeatures=%s" % self.local_features
        ret += ":: localScore=%f" % self.local_score
        return ret
