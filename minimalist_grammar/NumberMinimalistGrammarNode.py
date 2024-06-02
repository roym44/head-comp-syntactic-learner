import re
import copy

NODE_RE_PATTERN = r"""
    (?P<substring>.+)    # The substring of the input this node represents.
    :\ ?                 # A separator.
    (?P<features>.+)     # The features this node has.
"""
NODE_RE = re.compile(NODE_RE_PATTERN, re.VERBOSE)

FEATURES_DELIMITER = ' '
SELECT_PREFIX = '='
LICENSOR_PREFIX = '+'
LICENSEE_PREFIX = '-'

class NodeException(Exception): pass

class NumberMinimalistGrammarNode(object):
    
    def __init__(self, substring, base, selects, licensors, licensees):
        self.substring = substring
        self.base = base
        self.selects = selects
        self.licensors = licensors
        self.licensees = licensees
        
    def has_features(self):
        # Returns whether this node has features other than the base.
        return self.selects or self.licensors or self.licensees
        
    def __eq__(self, other):
        # return self.substring == other.substring and self.features == other.features
        return (self.substring == other.substring and
               self.base == other.base and
               self.selects == other.selects and
               self.licensors == other.licensors and
               self.licensees == other.licensees)
               
    def __ne__(self, other):
        return not (self == other)
        
    def __str__(self):
        return "%s: %s =%s +%s -%s" % (self.substring, self.base, self.selects, self.licensors, self.licensees)
        
    def __repr__(self):
        return "%s: %s =%s +%s -%s" % (self.substring, self.base, self.selects, self.licensors, self.licensees)
