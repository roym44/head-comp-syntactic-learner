import re
import copy

from NumberMinimalistGrammarNode import NumberMinimalistGrammarNode

SUBSTRING_DELIMITER = ' '

# The char we use to signify the empty string.
EMPTY_STRING = [(0, 0)]
BLANK_NODE = '*'

TYPE_SIMPLE = 0
TYPE_COMPLEX = 1

TREE_RE_PATTERN = r"""
    \[                  # Opening brace.
      (?P<nodes>.+)     # Anything for now, will be expanded in the node RE.
    \]                  # Closing brace.
      (?P<type>[%s%s])  # Type (simple/complex).
    """ % (TYPE_SIMPLE, TYPE_COMPLEX)
TREE_RE = re.compile(TREE_RE_PATTERN, re.VERBOSE)

NODES_DELIMITER = ', '

MERGE_TYPE_1 = 1
MERGE_TYPE_2 = 2

WITH_NESTED_DERIVATION = False

class TreeException(Exception): pass

class NumberMinimalistGrammarTree(object):
    
    # I assume that the tree gets a list of nodes and a type (simple/complex).
    def __init__(self, nodes, type, direction = "right"):
        self.nodes = nodes
        self.type = type
            
        # The number of items in the derivation.
        self.derivation_length = 0
        # The size of the encoding for the derivation (see MinimalistGrammarAnnealer.get_sentence_length).
        self.derivation_size = 0
        
        if WITH_NESTED_DERIVATION:
            self.nested_derivation = (self, "Lexicon")
        self.composing_items = {self}
            
        self.hash = hash(self)
        
        # If another tree is merged to this one, this property determines whether
        # it merges to the right (default Minimalist Grammars behaviour) or to the left.
        # This only applies to the first merge, the second merge will be to the left, as usual.
        # In a movement this works the opposite way, moving to the left for "right" and to the right for "left".
        self.complement_merge_direction = direction
        
    @property
    def head(self):
        return self.nodes[0]
        
    @property
    def other_nodes(self):
        return self.nodes[1:]
    
    def is_simple(self):
        return self.type == TYPE_SIMPLE
        
    def is_complex(self):
        return self.type == TYPE_COMPLEX
        
    # Returns None if unable to merge.
    def merge(self, selected_tree):
        if self.substrings_overlap(selected_tree):
            return None
    
        # Changed to make the order matter, the leftmost select feature has to be merged first.
        if not self.head.selects or selected_tree.head.base != self.head.selects[0]:
            return None # Trees aren't mergable.
            
        if selected_tree.head.selects or selected_tree.head.licensors:
            # A tree with licensors or select features cannot be merged, it has no way to get rid of those features.
            return None
        
        if selected_tree.head.has_features():
            # This subtree will have to move later to get its licensees.
            result = self.merge_3(selected_tree)
        else:
            # The selected tree will not move and can be joined to the head.
            if self.is_simple():
                result = self.merge_1(selected_tree)
            else: # This tree is complex.
                result = self.merge_2(selected_tree)
                
        if result is None:
            return None
        
        if WITH_NESTED_DERIVATION:
            result.nested_derivation = (result, "Merge", self.nested_derivation, selected_tree.nested_derivation)
        result.composing_items = self.composing_items | selected_tree.composing_items
            
        result.derivation_length = self.derivation_length + selected_tree.derivation_length + 1
        # Size + 2 because it's a merge operation.
        result.derivation_size = self.derivation_size + selected_tree.derivation_size + 2
                
        result.complement_merge_direction = self.complement_merge_direction
        return result
                
    def merge_1(self, selected_tree):
        return self.easy_merge(selected_tree, MERGE_TYPE_1)
        
    def merge_2(self, selected_tree):
        return self.easy_merge(selected_tree, MERGE_TYPE_2)
                
    def easy_merge(self, selected_tree, merge_type):
        # This works for both Merge-1 and Merge-2.
        result = NumberMinimalistGrammarTree([], TYPE_SIMPLE)
        new_head = NumberMinimalistGrammarNode(None, None, [], [], [])
        new_head.base = self.head.base
        
        new_head.selects = copy.deepcopy(self.head.selects)
        # This will remove the first occurrence which is what we want.
        new_head.selects = new_head.selects[1:]
        
        new_head.licensors = self.head.licensors
        new_head.licensees = self.head.licensees
        
        if merge_type == MERGE_TYPE_1:
            new_head.substring = self.join_substrings(self.head.substring, selected_tree.head.substring)
        elif merge_type == MERGE_TYPE_2:
            new_head.substring = self.join_substrings(selected_tree.head.substring, self.head.substring)
        else:
            raise TreeException("Invalid merge type (%s) for %s, %s" % (merge_type, self, selected_tree))
            
        if new_head.substring is None:
            return None
        
        other_nodes = copy.deepcopy(self.other_nodes) + copy.deepcopy(selected_tree.other_nodes)
        
        result.type = TYPE_COMPLEX
        result.nodes = [new_head] + other_nodes
        
        result.hash = hash(result)
        
        return result
        
    def merge_3(self, selected_tree):
        if self.is_head_misplaced(selected_tree):
            return None
        
        new_self = copy.deepcopy(self)
        new_selected = copy.deepcopy(selected_tree)
        
        # This will remove the first occurrence which is what we want.
        new_self.head.selects = new_self.head.selects[1:]
        new_selected.head.base = None
        
        result = NumberMinimalistGrammarTree([], TYPE_SIMPLE)
        result.type = TYPE_COMPLEX
        if new_self.is_simple():
            result.nodes = new_self.nodes + new_selected.nodes
        else: # It is complex
            result.nodes = [new_self.head] + new_selected.nodes + new_self.other_nodes
            
        result.hash = hash(result)
        
        return result
        
    def substrings_overlap(self, selected_tree):
        for self_node in self.nodes:
            for selected_node in selected_tree.nodes:
                if self_node.substring[0][1] <= selected_node.substring[0][0] or self_node.substring[0][0] >= selected_node.substring[0][1]:
                    pass
                else:
                    return True
        return False
        
    def is_head_misplaced(self, selected_tree):
        # If the selected node moves then the substrings should eventually come befor the selector's head.
        for node in selected_tree.nodes:
            if self.complement_merge_direction == "right":
                if node.substring[0][0] >= self.head.substring[0][1]:
                    return True
            else: # Merge direction is "left".
                if node.substring[0][1] <= self.head.substring[0][0]:
                    return True
        return False
        
    # Returns None if unable to move.
    def move(self):
        if self.is_simple():
            # A simple tree can't move (clearly).
            return None
        if not self.head.licensors:
            # The head doesn't allow movement.
            return None
            
        movable = False
        for node in self.other_nodes:
            for licensee in node.licensees:
                if licensee in self.head.licensors:
                    movable = True
                    moved_node = node
                    break
        if not movable:
            return None
        
        if len(moved_node.licensees) == 1:
            result = self.move_1(moved_node)
        else:
            # There is more than one. There can't be zero because the node wouldn't have been chosen.
            result = self.move_2(moved_node)
            
        if result is None:
            return None
            
        if WITH_NESTED_DERIVATION:
            result.nested_derivation = (result, "Move", self.nested_derivation)
        result.composing_items = self.composing_items
        result.derivation_length = self.derivation_length + 1
        result.derivation_size = self.derivation_size + 1
        
        result.complement_merge_direction = self.complement_merge_direction
        
        return result
            
    def move_1(self, moved_node):
        new_tree = copy.deepcopy(self)
        new_tree.nodes.remove(moved_node)
        new_tree.head.licensors.remove(moved_node.licensees[0]) # This is Move-1 so there is exactly one.
        
        new_tree.head.substring = self.join_substrings(moved_node.substring, new_tree.head.substring)
        
        if new_tree.head.substring is None:
            return None
        
        new_tree.hash = hash(new_tree)
        
        return new_tree
        
    def move_2(self, moved_node):
        new_tree = copy.deepcopy(self)
        node_index = new_tree.nodes.index(moved_node)
        
        for licensee in moved_node.licensees:
            if licensee in new_tree.head.licensors:
                new_tree.nodes[node_index].licensees.remove(licensee)
                new_tree.head.licensors.remove(licensee)
                break
                
        new_tree.hash = hash(new_tree)
                
        return new_tree
        
    def join_substrings(self, substring_1, substring_2):
        if EMPTY_STRING == substring_1:
            # If we have the empty string we won't concatenate it.
            return substring_2
        elif EMPTY_STRING == substring_2:
            # If we have the empty string we won't concatenate it.
            return substring_1
        else:
            # Both substrings are tuples of indices of words in the original sentence.
            # If they aren't consecutive then there is no point in joining them.
            joined_substring = []
            for sub_1 in substring_1:
                for sub_2 in substring_2:
                    if self.complement_merge_direction == "right" and sub_1[1] == sub_2[0]:
                        joined_substring += [(sub_1[0], sub_2[1])]
                    if self.complement_merge_direction == "left" and sub_2[1] == sub_1[0]:
                        joined_substring += [(sub_2[0], sub_1[1])]
            
            if joined_substring:
                return joined_substring
            else:
                return None
        
    def size(self):
        return sum([node.substring[0][1] - node.substring[0][0] for node in self.nodes if node.substring != EMPTY_STRING])
        
    def __eq__(self, other):
        return self.nodes == other.nodes and \
               self.type == other.type and \
               self.complement_merge_direction == other.complement_merge_direction

    def __ne__(self, other):
        return not (self == other)
        
    def __str__(self):
        return '[%s]%s' % (NODES_DELIMITER.join([str(node) for node in self.nodes]), self.type)
        
    def __repr__(self):
        return '[%s]%s' % (NODES_DELIMITER.join([str(node) for node in self.nodes]), self.type)
        
def test_actions():
    print "\nMerge-1"
    tree1 = MinimalistGrammarTree("[every:=n d -case]s")
    tree2 = MinimalistGrammarTree("[man:n]s")
    merged = tree1.merge(tree2)
    
    print "Tree 1:", tree1
    print "Tree 2:", tree2
    print "Merged:", merged
    
    print "\nMerge-2"
    tree1 = MinimalistGrammarTree("[s1:=a b, s2 s3:-f1]c")
    tree2 = MinimalistGrammarTree("[t1:a]s")
    merged = tree1.merge(tree2)
    
    print "Tree 1:", tree1
    print "Tree 2:", tree2
    print "Merged:", merged

    print "\nMerge-3"
    tree1 = MinimalistGrammarTree("[kiss:=d vt -v]s")
    tree2 = MinimalistGrammarTree("[every girl:d -case]c")
    merged = tree1.merge(tree2)
    
    print "Tree 1:", tree1
    print "Tree 2:", tree2
    print "Merged:", merged
    
    print "\nMove-1:"
    tree = MinimalistGrammarTree("[e:+k =d pred, praise:-v, Lavinia:-k]c")
    moved = tree.move()
    print "Tree:", tree
    print "Moved:", moved
    
    print "\nMove-2:"
    tree = MinimalistGrammarTree("[s1:+f1 a, s2 s3: -f1 -f2]c")
    moved = tree.move()
    print "Tree:", tree
    print "Moved:", moved
    
def linguistic_example():
    tree_23 = MinimalistGrammarTree("[Lavinia:d -k]s")
    tree_24 = MinimalistGrammarTree("[Titus:d -k]s")
    tree_25 = MinimalistGrammarTree("[praise:=d vt -v]s")
    tree_26 = MinimalistGrammarTree("[s:=pred +v +k i]s")
    tree_27 = MinimalistGrammarTree("[e:=i c]s")
    tree_28 = MinimalistGrammarTree("[e:=vt +k =d pred]s")
    
    tree_29 = tree_25.merge(tree_23)
    print tree_29
    tree_30 = tree_28.merge(tree_29)
    print tree_30
    tree_31 = tree_30.move()
    print tree_31
    tree_32 = tree_31.merge(tree_24)
    print tree_32
    tree_33 = tree_26.merge(tree_32)
    print tree_33
    tree_34 = tree_33.move()
    print tree_34
    tree_35 = tree_34.move()
    print tree_35
    tree_36 = tree_27.merge(tree_35)
    print tree_36

def abstract_example():
    tree_37 = MinimalistGrammarTree("[@: c]s")
    tree_38 = MinimalistGrammarTree("[@: =a +d +b +a c]s")
    tree_39 = MinimalistGrammarTree("[a: =b a -a]s")
    tree_40 = MinimalistGrammarTree("[b:=d b -b]s")
    tree_41 = MinimalistGrammarTree("[d: d -d]s")
    tree_42 = MinimalistGrammarTree("[a:=b +a a -a]s")
    tree_43 = MinimalistGrammarTree("[b:=d +b b -b]s")
    tree_44 = MinimalistGrammarTree("[d:=a +d d -d]s")
    
    tree_45 = tree_40.merge(tree_41)
    print "45:", tree_45
    tree_46 = tree_39.merge(tree_45)
    print "46:", tree_46
    tree_47 = tree_44.merge(tree_46)
    print "47:", tree_47
    tree_48 = tree_47.move()
    print "48:", tree_48
    tree_49 = tree_43.merge(tree_48)
    print "49:", tree_49
    tree_50 = tree_49.move()
    print "50:", tree_50
    tree_51 = tree_42.merge(tree_50)
    print "51:", tree_51
    tree_52 = tree_51.move()
    print "52:", tree_52
    tree_53 = tree_38.merge(tree_52)
    print "53:", tree_53
    tree_54 = tree_53.move()
    print "54:", tree_54
    tree_55 = tree_54.move()
    print "55:", tree_55
    tree_56 = tree_55.move()
    print "56:", tree_56

if __name__ == '__main__':
    a = NumberMinimalistGrammarTree([NumberMinimalistGrammarNode((0,1), 0, [1], [], [])], TYPE_SIMPLE)
    b = NumberMinimalistGrammarTree([NumberMinimalistGrammarNode((1,2), 1, [], [], [])], TYPE_SIMPLE)
    print a.merge(b)
