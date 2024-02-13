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

class MinimalistGrammarNode(object):
    
    def __init__(self, node_string = None):
        if not node_string:
            self.base = None
            self.selects = []
            self.licensors = []
            self.licensees = []
        else:
            self.string_to_node(node_string)
        
    def string_to_node(self, node_string):
        match = NODE_RE.match(node_string)
        if not match:
            raise NodeException("Failed to parse node string - %s" % (node_string, ))
        self.substring = match.group("substring")
        
        features_string = match.group("features")
        self.features = features_string.split(FEATURES_DELIMITER)
        
    def has_features(self):
        # Returns whether this node has features other than the base.
        return self.selects or self.licensors or self.licensees
        
    @property
    def features(self):
        if self.base:
            feats = [self.base, ]
        else:
            feats = []
        feats += [SELECT_PREFIX + select for select in self.selects]
        feats += [LICENSOR_PREFIX + licensor for licensor in self.licensors]
        feats += [LICENSEE_PREFIX + licensee for licensee in self.licensees]
        return feats
        
    @features.setter
    def features(self, feats):
        bases = []
        self.selects = []
        self.licensors = []
        self.licensees = []
        
        for feature in feats:
            if feature.startswith(SELECT_PREFIX):
                self.selects.append(feature[len(SELECT_PREFIX):])
            elif feature.startswith(LICENSOR_PREFIX):
                self.licensors.append(feature[len(LICENSOR_PREFIX):])
            elif feature.startswith(LICENSEE_PREFIX):
                self.licensees.append(feature[len(LICENSEE_PREFIX):])
            else:
                bases.append(feature)
        
        if len(bases) > 1:
            raise NodeException("Node has more than one base - %s" % (feats, ))
            
        if bases:
            self.base = bases[0]
        else:
            self.base = None
            
    def __eq__(self, other):
        return self.substring == other.substring and self.features == other.features
        
    def __ne__(self, other):
        return not (self == other)
        
    def __str__(self):
        return "%s: %s" % (self.substring, FEATURES_DELIMITER.join(self.features))
        
    def __repr__(self):
        return "%s: %s" % (self.substring, FEATURES_DELIMITER.join(self.features))
