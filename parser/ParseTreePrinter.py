import os
import time
from igraph import Graph, plot

PICS_FOLDER = "resources"

# This function expects the following structure:
# step is a tuple with at least two fields.
# The first is the type - either "Lexicon", "Move" or "Merge".
# The second is the MinimalistGrammarTree string of that node.
# If the type is Lexicon then there are no other fields.
# If the type is Move then the third field is a step object of the previous node that moved to become the current node.
# If the type is Merge then the third and fourth fields are step objects of the two previous nodes that merged to become the current node.
# The type will be the label of the edges.
def build_derivation_step(tree, step, translation_func = None):
    if translation_func is None:
        node_name = step[0]
    else:
        node_name = str(translation_func(step[0]))
    step_type = step[1]
    
    vertex_id = tree.vcount()
    tree.add_vertex(node_name)
    
    if 2 == len(step): # Lexicon
        pass
    
    elif 3 == len(step): # Move
        preceding_step = step[2]
        preceding_node = build_derivation_step(tree, preceding_step, translation_func = translation_func)
        tree.add_edge(vertex_id, preceding_node, label = step_type)
        
    elif 4 == len(step): # Merge
        first_step = step[2]
        second_step = step[3]
        first_node = build_derivation_step(tree, first_step, translation_func = translation_func)
        second_node = build_derivation_step(tree, second_step, translation_func = translation_func)
        tree.add_edge(vertex_id, first_node)
        tree.add_edge(vertex_id, second_node, label = step_type)
        
    else:
        raise ValueError('Invalid number of child nodes.')
        
    return vertex_id

def print_parse_tree(sentence, derivation, save_to_file = True, translation_func = None):
    tree = Graph()
    
    final_node = build_derivation_step(tree, derivation, translation_func = translation_func)
    
    # Second parameter is the index of the vertex that should be the root of the tree.
    layout = tree.layout_reingold_tilford(mode = "all", root = [final_node]) #rootlevel = ???)
    
    visual_style = {}
    visual_style["vertex_size"] = 10
    visual_style["vertex_color"] = ["blue" for v in tree.vs]
    visual_style["vertex_label"] = tree.vs["name"]
    visual_style["vertex_label_dist"] = -4
    visual_style["layout"] = layout
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 100
    
    plot(tree, **visual_style)
    if save_to_file:
        time_str = time.strftime("%Y_%m_%d__%H_%M_%S - ")
        file_name = time_str + sentence + ".png"
        file_path = os.path.join(PICS_FOLDER, file_name)
        plot(tree, file_path, **visual_style)
        
if __name__ == '__main__':
    sample_derivation = ("who John saw", "Move", ("John saw who", "Merge", ("John", "Lexicon"), ("saw who", "Merge", ("saw", "Lexicon"), ("who", "Lexicon"))))
    print_parse_tree("who John saw", sample_derivation, save_to_file = False)
    