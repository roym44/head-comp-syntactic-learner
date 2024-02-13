import re
import copy

from MinimalistGrammarNode import MinimalistGrammarNode

SUBSTRING_DELIMITER = ' '

# The char we use to signify the empty string.
EMPTY_STRING = '@'
BLANK_NODE = '*'

TYPE_SIMPLE = "s"
TYPE_COMPLEX = "c"

TREE_RE_PATTERN = r'''
    \[                    # Opening brace.
      (?P<direction>[<>]) # Complement merge direction.
      (?P<nodes>.+)       # Anything for now, will be expanded in the node RE.
    \]                    # Closing brace.
      (?P<type>[%s%s])    # Type (simple/complex).
    ''' % (TYPE_SIMPLE, TYPE_COMPLEX)
TREE_RE = re.compile(TREE_RE_PATTERN, re.VERBOSE)

NODES_DELIMITER = ', '

MERGE_TYPE_1 = "Merge-1"
MERGE_TYPE_2 = "Merge-2"

WITH_NESTED_DERIVATION = True

class TreeException(Exception): pass

class MinimalistGrammarTree(object):
    
    def __init__(self, tree_string = None):
        self.complement_merge_direction = "right"
        
        if not tree_string:
            self.type = TYPE_SIMPLE
            self.nodes = []
        else:
            self.string_to_tree(tree_string)
            
        self.derivation = []
        if WITH_NESTED_DERIVATION:
            self.nested_derivation = (tree_string, "Lexicon")
        
    def string_to_tree(self, tree_string):
        match = TREE_RE.match(tree_string)
        if not match:
            raise TreeException("Failed to parse tree string - %s" % (tree_string, ))
        self.type = match.group("type")
        
        if match.group("direction") == ">":
            self.complement_merge_direction = "right"
        else: # "<"
            self.complement_merge_direction = "left"
        
        nodes_string = match.group("nodes")
        node_strings = nodes_string.split(NODES_DELIMITER)
        
        if len(node_strings) < 1:
            raise TreeException("Not enough nodes - %s" % (tree_string, ))
        if self.type == TYPE_SIMPLE and len(node_strings) != 1:
            raise TreeException("Too many nodes for a simple tree - %s" % (tree_string, ))
        
        self.nodes = []
        for node_string in node_strings:
            node = MinimalistGrammarNode(node_string)
            self.nodes.append(node)
            
        # Only the head node needs to have a base, the others don't.
        if not self.head.base:
            raise TreeException("Head node should have a base - %s" % (tree_string, ))
        for node in self.other_nodes:
            if node.base:
                raise TreeException("Non-head node should not have a base - %s (node - %s)" % (tree_string, node))
                
        self.hash = hash(str(self))
        
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
                
        if WITH_NESTED_DERIVATION:
            result.nested_derivation = (str(result), "Merge", self.nested_derivation, selected_tree.nested_derivation)
            
        derivations = self.derivation + selected_tree.derivation + ["Merge: %s + %s = %s" % (self, selected_tree, result)]
        result.derivation = []
        for derivation in derivations:
            if derivation:
                result.derivation.append(derivation)
                
        result.complement_merge_direction = self.complement_merge_direction
        return result
                
    def merge_1(self, selected_tree):
        return self.easy_merge(selected_tree, MERGE_TYPE_1)
        
    def merge_2(self, selected_tree):
        return self.easy_merge(selected_tree, MERGE_TYPE_2)
                
    def easy_merge(self, selected_tree, merge_type):
        # This works for both Merge-1 and Merge-2.
        result = MinimalistGrammarTree()
        new_head = MinimalistGrammarNode()
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
        
        other_nodes = copy.deepcopy(self.other_nodes) + copy.deepcopy(selected_tree.other_nodes)
        
        result.type = TYPE_COMPLEX
        result.nodes = [new_head] + other_nodes
        
        result.hash = hash(str(result))
        
        return result
        
    def merge_3(self, selected_tree):
        new_self = copy.deepcopy(self)
        new_selected = copy.deepcopy(selected_tree)
        
        # This will remove the first occurrence which is what we want.
        new_self.head.selects = new_self.head.selects[1:]
        new_selected.head.base = None
        
        result = MinimalistGrammarTree()
        result.type = TYPE_COMPLEX
        if new_self.is_simple():
            result.nodes = new_self.nodes + new_selected.nodes
        else: # It is complex
            result.nodes = [new_self.head] + new_selected.nodes + new_self.other_nodes
            
        result.hash = hash(str(result))
        
        return result
        
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
            
        if WITH_NESTED_DERIVATION:
            result.nested_derivation = (str(result), "Move", self.nested_derivation)
        result.derivation.append("Move: %s = %s" % (self, result))
        
        result.complement_merge_direction = self.complement_merge_direction
        
        return result
            
    def move_1(self, moved_node):
        new_tree = copy.deepcopy(self)
        new_tree.nodes.remove(moved_node)
        new_tree.head.licensors.remove(moved_node.licensees[0]) # This is Move-1 so there is exactly one.
        new_tree.head.substring = self.join_substrings(moved_node.substring, new_tree.head.substring)
        
        new_tree.hash = hash(str(new_tree))
        
        return new_tree
        
    def move_2(self, moved_node):
        new_tree = copy.deepcopy(self)
        node_index = new_tree.nodes.index(moved_node)
        
        for licensee in moved_node.licensees:
            if licensee in new_tree.head.licensors:
                new_tree.nodes[node_index].licensees.remove(licensee)
                new_tree.head.licensors.remove(licensee)
                break
                
        new_tree.hash = hash(str(new_tree))
                
        return new_tree
        
    def join_substrings(self, substring_1, substring_2):
        if substring_1 == EMPTY_STRING:
            # If we have the empty string we won't concatenate it.
            return substring_2
        elif substring_2 == EMPTY_STRING:
            # If we have the empty string we won't concatenate it.
            return substring_1
        else:
            # We have two proper substrings.
            # return SUBSTRING_DELIMITER.join([substring_1, substring_2])
            
            if self.complement_merge_direction == "right":
                return SUBSTRING_DELIMITER.join([substring_1, substring_2])
            elif self.complement_merge_direction == "left":
                return SUBSTRING_DELIMITER.join([substring_2, substring_1])
        
    def size(self):
        return len(SUBSTRING_DELIMITER.join([node.substring for node in self.nodes if node.substring != EMPTY_STRING]))
        
    # Verifies if the tree is possible for the given input.
    def is_possible_for_input(self, input):
        for node in self.nodes:
            if node.substring != EMPTY_STRING and node.substring not in input:
                return False
        return True
        
    def is_loop(self):
        count = 0
        for item in self.derivation:
            if str(self) in item:
                count += 1
        if count > 1:
            return True
        else:
            return False
        
    def __eq__(self, other):
        return self.hash == other.hash
        
    def __ne__(self, other):
        return not (self == other)
        
    def __str__(self):
        if self.complement_merge_direction == "right":
            direction = ">"
        elif self.complement_merge_direction == "left":
            direction = "<"
        else:
            raise TreeException("Invalid merge direction - %s" % (self.complement_merge_direction, ))
        return '[%s%s]%s' % (direction, NODES_DELIMITER.join([str(node) for node in self.nodes]), self.type)
        
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
        return self.hash
        
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
    tree_0 = MinimalistGrammarTree("[>@: IP]s")
    tree_1 = MinimalistGrammarTree("[>a:IP =IP +A, a: -A]c")
    tree_2 = MinimalistGrammarTree("[>b:IP =IP +B, b: -B]c")
    tree_2 = tree_2.merge(tree_0)
    print tree_2
    print tree_1.merge(tree_2)
    tree_3 = tree_1.move()
    print tree_3
    tree_4 = tree_2.move()
    print tree_4
    print tree_1.merge(tree_4)
    print tree_3.merge(tree_2)
    print tree_3.merge(tree_4)
    
