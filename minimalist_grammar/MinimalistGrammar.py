from functools import cmp_to_key
from minimalist_grammar import MinimalistGrammarTree


class MinimalistGrammar(object):

    def __init__(self, lexicon):
        self.licensors = None
        self.bases = None
        self.substrings = None
        self.lexicon = lexicon
        # TODO: new parameter, consider removing
        self.failed_parsing = 0
        self.get_features()

    def get_features(self):
        self.substrings = []
        self.bases = []
        self.licensors = []
        for tree in self.lexicon:
            for node in tree.nodes:
                self.substrings.append(node.substring)
                if node.base:
                    self.bases.append(node.base)
                for select in node.selects:
                    self.bases.append(select)
                for licensor in node.licensors + node.licensees:
                    self.licensors.append(licensor)
        self.substrings = list(set(self.substrings))
        self.bases = list(set(self.bases))
        self.licensors = list(set(self.licensors))

    def __str__(self):
        return str(self.lexicon)

    def __eq__(self, other):
        return set([str(item) for item in self.lexicon]) == set([str(item) for item in other.lexicon])

    def __ne__(self, other):
        return not (self == other)

    def get_sorted_lexicon(self):
        return sorted(self.lexicon, key=cmp_to_key(compare_for_susbtrings))


def get_grammar_from_string(grammar_string):
    tree_strings = grammar_string.strip()[1:-1].split(', [')
    for i in range(1, len(tree_strings)):
        tree_strings[i] = '[' + tree_strings[i]
    tree_list = [MinimalistGrammarTree.MinimalistGrammarTree(tree_str) for tree_str in tree_strings]
    return MinimalistGrammar(tree_list)


def compare_for_susbtrings(one, two):
    substrings = ["@",
                  "Jerry", "George", "Elaine", "Kramer",
                  "ran", "walked", "read", "wrote",
                  "liked", "saw", "loved", "hated",
                  "with", "by", "above", "under",
                  "that",
                  "knows", "says", "thinks", "assumes"]
    if substrings.index(one.head.substring) > substrings.index(two.head.substring):
        return 1
    elif substrings.index(one.head.substring) < substrings.index(two.head.substring):
        return -1
    else:
        if len(str(one)) > len(str(two)):
            return 1
        elif len(str(one)) < len(str(two)):
            return -1
        else:
            return 0
