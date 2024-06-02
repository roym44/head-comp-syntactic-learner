
import time
import math
import random

import BlankGrammars
from parser.NumberBottomUpParser import NumberBottomUpParser
from minimalist_grammar.MinimalistGrammarTree import *
from minimalist_grammar.MinimalistGrammarNode import MinimalistGrammarNode

MAX_GRAMMAR_LENGTH = 1200

class AnnealerException(Exception): pass

def default_log(line):
    print(line)

class MinimalistGrammarAnnealer(object):
    
    def __init__(self, input, blank_grammar, learner_type, log_function = default_log, separator = SUBSTRING_DELIMITER):
        self.input = input
        self.input_parsing_dict = {}
        self.separator = separator
        self.category = 1
        self.blank_grammar = blank_grammar
        
        self.learner_type = learner_type
        self.set_learner_type()
        
        self.log = log_function
        
        self.split_to_words()
        
    def set_learner_type(self):
        # NOTE: More modifications to this list are done in random_neighbour below.
        self.neighbour_functions = [self.delete,
                                    self.delete,
                                    
                                    self.add_any_lexical_item,
                                    self.add_probable_lexical_item
                                    ]
        if self.learner_type == "Kayne":
            pass
        elif self.learner_type == "Language":
            self.neighbour_functions.append(self.change_language_direction_with_flip)
        elif self.learner_type == "Category":
            self.neighbour_functions.append(self.change_category_direction_with_flip)
        elif self.learner_type == "Word":
            self.neighbour_functions.append(self.change_word_direction_with_flip)
            self.neighbour_functions.append(self.change_word_direction_with_flip)
            self.neighbour_functions.append(self.change_category_direction_with_flip)
            self.neighbour_functions.append(self.change_language_direction_with_flip)
        else:
            raise AnnealerException("Unexpected learner type - %s" % (self.learner_type, ))
        
    def split_to_words(self):
        input_string = self.separator.join(self.input)
        if self.separator == '':
            # This means we treat letters as words.
            self.words = list(input_string)
        else:
            self.words = input_string.split(self.separator)
        self.words = list(set(self.words))
    
    def get_initial_hypothesis(self):
        # Just deleting from a blank grammar:
        lexicon = []
        for tree in self.blank_grammar.lexicon:
            tree_str = str(tree)
            if BLANK_NODE in tree_str:
                for word in self.words:
                    new_str = tree_str.replace(BLANK_NODE, word)
                    new_tree = MinimalistGrammarTree(new_str)
                    new_tree.complement_merge_direction = "right"
                    lexicon.append(new_tree)
            else:
                lexicon.append(tree)
        
        return MinimalistGrammar(sorted(lexicon))
        
    def random_neighbour(self, hypothesis):
        neighbour = None
        retry_count = 0
        
        if len(hypothesis.lexicon) > 70:
            neighbour_functions = self.neighbour_functions + [self.delete,
                                                              self.delete,
                                                              self.delete,
                                                              self.delete,
                                                              self.delete,
                                                              self.delete,
                                                              self.delete,
                                                              self.delete,
                                                              self.delete]
        elif len(hypothesis.lexicon) < 50:
            neighbour_functions = self.neighbour_functions + [self.add_and_delete, self.add_probable_and_delete]
        else:
            neighbour_functions = self.neighbour_functions + [self.add_and_delete, self.add_probable_and_delete]
            
        while neighbour is None and retry_count < 10:
            option = random.choice(neighbour_functions)
            neighbour, energy = option(hypothesis)
            retry_count += 1
        if retry_count == 10:
            self.log("Couldn't find better hypothesis.")
            return None, None
        return neighbour, energy
    
    def add_and_delete(self, hypothesis):
        for i in range(10):
            self.log("Trying to add and delete")
            grammar, energy = self.add_any_lexical_item(hypothesis)
            if grammar:
                grammar, energy = self.delete(grammar)
            if grammar and grammar != hypothesis:
                self.log("Added and deleted")
                return grammar, energy
                
        return None, None
        
    def add_probable_and_delete(self, hypothesis):
        for i in range(10):
            self.log("Trying to add probable and delete")
            grammar, energy = self.add_probable_lexical_item(hypothesis)
            if grammar:
                grammar, energy = self.delete(grammar)
            if grammar and grammar != hypothesis:
                self.log("Added and deleted")
                return grammar, energy
                
        return None, None
        
    def delete(self, hypothesis):
        for i in range(10):
            grammar, energy = self.delete_once(hypothesis)
            if grammar:
                return grammar, energy
        return grammar, energy
        
    def delete_once(self, hypothesis):
        # Just making a copy.
        new_lexicon = hypothesis.lexicon[:]
        removed = new_lexicon.pop(random.randrange(0, len(new_lexicon)))
        
        self.log("Trying to delete: " + str(removed))
        if removed.head.substring == EMPTY_STRING:
            return None, None
        
        new_grammar = MinimalistGrammar(new_lexicon)
        try:
            energy = self.energy(new_grammar, deleted = removed)
        except KeyboardInterrupt as e:
            raise e
        except:
            return None, None
        self.log("Deleting: " + str(removed))
        return new_grammar, energy
        
    def add_any_lexical_item(self, hypothesis):
        self.log("Add lexical item:")
        blank_lexicon_without_empty_string = [category for category in self.blank_grammar.lexicon if EMPTY_STRING not in str(category)]
        for i in range(10):
            grammar, energy = self.add_lexical_item_once(hypothesis, blank_lexicon_without_empty_string)
            if grammar:
                return grammar, energy
        return grammar, energy
        
    def add_probable_lexical_item(self, hypothesis):
        self.log("Add probable item:")
        blank_lexicon_without_empty_string = [category for category in self.blank_grammar.lexicon if EMPTY_STRING not in str(category)]
        hypothesis_without_substrings = [str(category).split(":")[1] for category in hypothesis.lexicon]
        probable_categories = [category for category in blank_lexicon_without_empty_string if str(category).split(":")[1] in hypothesis_without_substrings]
        for i in range(10):
            grammar, energy = self.add_lexical_item_once(hypothesis, probable_categories)
            if grammar:
                return grammar, energy
        return grammar, energy
        
    def add_lexical_item_once(self, hypothesis, category_list):
        category = random.choice(category_list)
        tree_str = str(category)
        if BLANK_NODE in tree_str:
            word = random.choice(self.words)
            tree_str = tree_str.replace(BLANK_NODE, word)
        new_tree = MinimalistGrammarTree(tree_str)
        
        if self.learner_type == "Kayne":
            new_tree.complement_merge_direction = "right"
        elif self.learner_type == "Language":
            i = 0
            # Some non-empty item must exist because the input must be parsed.
            while hypothesis.lexicon[i].head.substring == EMPTY_STRING:
                i += 1
            new_tree.complement_merge_direction = hypothesis.lexicon[i].complement_merge_direction
        elif self.learner_type == "Category":
            i = 0
            # It's possible that some category has been deleted from the hypothesis.
            while i < len(hypothesis.lexicon) and (hypothesis.lexicon[i].head.substring == EMPTY_STRING or
                                                   hypothesis.lexicon[i].head.base != new_tree.head.base or
                                                   hypothesis.lexicon[i].head.selects != new_tree.head.selects):
                i += 1
            if i < len(hypothesis.lexicon):
                new_tree.complement_merge_direction = hypothesis.lexicon[i].complement_merge_direction
            else:
                # Merge direction will be the default - right.
                pass
        elif self.learner_type == "Word":
            i = 0
                
            # If this item or its flipped version is in the grammar then we won't add.
            for item in hypothesis.lexicon:
                if item.head.substring == new_tree.head.substring and item.head.base == new_tree.head.base and item.head.selects == new_tree.head.selects:
                    return None, None
            
            new_tree.complement_merge_direction = random.choice(["right", "left"])
            
        else:
            raise AnnealerException("Unexpected learner type - %s" % (self.learner_type, ))
        
        self.log("Trying to add item: " + str(new_tree))
        if str(new_tree) in [str(item) for item in hypothesis.lexicon]:
            return None, None
            
        # Just making a copy.
        new_lexicon = hypothesis.lexicon[:]
        new_lexicon.append(new_tree)
        new_grammar = MinimalistGrammar(new_lexicon)
        energy = self.energy(new_grammar, added = new_tree)
        self.log("Adding item: " + str(new_tree))
        return new_grammar, energy
                
    def delete_impossible_category(self, hypothesis):   
        word = random.choice(self.words)
        word_categories = []
        other_trees = []
        # Just making a copy.
        new_lexicon = hypothesis.lexicon[:]
        for tree in new_lexicon:
            if tree.nodes[0].substring == word:
                word_categories.append(tree)
            else:
                other_trees.append(tree)
        category_to_test = random.choice(word_categories)
        self.log("Testing the category " + str(category_to_test))
        grammar_to_test = MinimalistGrammar(other_trees + [category_to_test])
        try:
            # This should do what we want which is to only parse the sentences where the word appears.
            energy = self.energy(grammar_to_test, log = False, flipped_word = word)
        except AnnealerException:
            pass
        else:
            return None, None
        
        new_lexicon.remove(category_to_test)
        new_grammar = MinimalistGrammar(new_lexicon)
        try:
            energy = self.energy(new_grammar, deleted = category_to_test)
        except:
            return None, None
        self.log("Removing impossible category: " + str(category_to_test))
        return new_grammar, energy
        
    def flip_item_direction(self, item):
        current_direction = item.complement_merge_direction
        if current_direction == "right":
            new_direction = "left"
        elif current_direction == "left":
            new_direction = "right"
        else:
            raise AnnealerException("Invalid merge direction in hypothesis - %s" % (current_direction, ))
            
        if self.blank_grammar == BlankGrammars.KAYNE_GRAMMAR_WITH_HACK:
            # Copying.
            new_tree = MinimalistGrammarTree(str(item))
            if new_tree.nodes[0].substring != EMPTY_STRING:
                new_tree.complement_merge_direction = new_direction
            if len(new_tree.nodes) > 1: # One of these - [word: VP =DP +O, @: -O]c
                new_tree.nodes = new_tree.nodes[:1]
                new_tree.head.licensors = []
                new_tree.type = TYPE_SIMPLE
            elif new_tree.head.substring != EMPTY_STRING and new_tree.head.selects: # One of these - [word: VP =DP]s
                new_tree.nodes.append(MinimalistGrammarNode("%s: -O" % (EMPTY_STRING, )))
                new_tree.head.licensors = ['O']
                new_tree.type = TYPE_COMPLEX
            else: # Otherwise - [word: DP]s or [@: IP =DP =VP]
                pass
        elif self.blank_grammar == BlankGrammars.KAYNE_GRAMMAR_WITH_EMPTY_DP:
            category_flip_dict = {"CP =IP]s" : "CP =IP +Comp -Oc]s",
                                  "VP =DP]s" : "VP =DP +O]s",
                                  "VP =CP]s" : "VP =CP +Oc]s",
                                  "PP =DP]s" : "PP =DP +O]s",
                                  "CP =IP +Comp -Oc]s" : "CP =IP]s",
                                  "VP =DP +O]s" : "VP =DP]s",
                                  "VP =CP +Oc]s" : "VP =CP]s",
                                  "PP =DP +O]s" : "PP =DP]s"}
            direction_and_substring, category = str(item).split(': ')
            if category in category_flip_dict:
                new_category = category_flip_dict[category]
            else:
                new_category = category
            
            if item.head.substring != EMPTY_STRING:
                new_tree = MinimalistGrammarTree(": ".join([direction_and_substring, new_category]))
                new_tree.complement_merge_direction = new_direction
            else:
                new_tree = MinimalistGrammarTree(str(item))
        else:
            raise AnnealerException("Unsupported blank grammar for flip.")
            
        return new_tree
        
    def change_language_direction_with_flip(self, hypothesis):
        new_lexicon = []
        
        # Empty string items don't change direction.
        i = 0
        while hypothesis.lexicon[i].nodes[0].substring == EMPTY_STRING:
            i += 1
        current_direction = hypothesis.lexicon[i].complement_merge_direction
        if current_direction == "right":
            new_direction = "left"
        elif current_direction == "left":
            new_direction = "right"
        else:
            raise AnnealerException("Invalid merge direction in hypothesis - %s" % (current_direction, ))
        
        for item in hypothesis.lexicon:
            if self.learner_type == "Language": # If we're in another type than items can be in different directions.
                # Empty string items don't change direction.
                if item.nodes[0].substring != EMPTY_STRING and len(item.head.selects) < 2 and item.complement_merge_direction != current_direction:
                    raise AnnealerException("Unexpected merge direction - expected: %s, found: %s" % (current_direction, item.complement_merge_direction))
                
            new_tree = self.flip_item_direction(item)
            
            new_lexicon.append(new_tree)
        
        new_grammar = MinimalistGrammar(new_lexicon)
        try:
            energy = self.energy(new_grammar)
        except AnnealerException:
            return None, None
            
        self.log("Changing language direction: %s -> %s" % (current_direction, new_direction))
        return new_grammar, energy
        
    def change_category_direction_with_flip(self, hypothesis):
        new_lexicon = []
        
        # No need to flip categories without select features - it won't make any difference.
        categories = set([item.head.base for item in hypothesis.lexicon if item.head.substring != EMPTY_STRING and len(item.head.selects) == 1])
        category_to_flip = random.choice(list(categories))
        category_items = [item for item in hypothesis.lexicon if item.nodes[0].base == category_to_flip and item.nodes[0].substring != EMPTY_STRING and len(item.head.selects) < 2]
        
        current_direction = category_items[0].complement_merge_direction
        if current_direction == "right":
            new_direction = "left"
        elif current_direction == "left":
            new_direction = "right"
        else:
            raise AnnealerException("Invalid merge direction in hypothesis - category: %s, direction: %s" % (category_to_flip, current_direction))
        
        for item in hypothesis.lexicon:
            
            if item in category_items:
                new_tree = self.flip_item_direction(item)
            else:
                new_tree = MinimalistGrammarTree(str(item))
                
            new_lexicon.append(new_tree)
        
        new_grammar = MinimalistGrammar(new_lexicon)
        try:
            energy = self.energy(new_grammar)
        except AnnealerException:
            return None, None
            
        self.log("Changing %s direction: %s -> %s" % (category_to_flip, current_direction, new_direction))
        return new_grammar, energy
    
    def change_word_direction_with_flip(self, hypothesis):
        new_lexicon = []
        
        # Get all words.
        words = set([item.head.substring for item in hypothesis.lexicon if item.head.substring != EMPTY_STRING and len(item.head.selects) < 2])
        word_to_flip = random.choice(list(words))
        word_items = [item for item in hypothesis.lexicon if item.head.substring == word_to_flip and len(item.head.selects) < 2]
        
        current_direction = word_items[0].complement_merge_direction
        if current_direction == "right":
            new_direction = "left"
        elif current_direction == "left":
            new_direction = "right"
        else:
            raise AnnealerException("Invalid merge direction in hypothesis - word: %s, direction: %s" % (word_to_flip, current_direction))
        
        # We only bother to flip items with selects features - otherwise the direction doesn't matter.
        item_to_flip = random.choice([item for item in hypothesis.lexicon if item.head.substring != EMPTY_STRING and item.head.selects])
        
        for item in hypothesis.lexicon:
            # If we flip [>liked: VP =DP]s, we also want to flip [>liked: VP =DP +O]
            # Otherwise we could have two items that do the same thing. With 'delete' it doesn't matter but with 'delete_impossible_category' it does.
            if item.head.substring == item_to_flip.head.substring and item.head.base == item_to_flip.head.base and item.head.selects == item_to_flip.head.selects:
                new_tree = self.flip_item_direction(item)
                flipped_item = new_tree
            else:
                new_tree = MinimalistGrammarTree(str(item))
                
            new_lexicon.append(new_tree)
        
        # If after flipping we get an item that is already in the hypothesis then there's no point to the flip.
        if str(flipped_item) in [str(item) for item in hypothesis.lexicon]:
            return None, None
        
        new_grammar = MinimalistGrammar(new_lexicon)
        try:
            energy = self.energy(new_grammar, flipped_word = item_to_flip.head.substring)
        except AnnealerException:
            return None, None
            
        self.log('Changing "%s" direction: -> %s' % (item_to_flip, flipped_item))
        return new_grammar, energy
        
    # Here I calculate the theoretical length of the grammar and the input.
    def energy(self, hypothesis, deleted = None, added = None, flipped_word = None, log = True):
        parsing_results = self.get_parsing_results(hypothesis, deleted = deleted, added = added, flipped_word = flipped_word)
        # The members of the grammar that took part in the parsing of some sentence.
        set_sum = lambda x, y: x | y
        parsing_grammar = hypothesis
        if log:
            self.log("Total number of possible derivations: " + str(sum([len(results) for results in parsing_results])))
        
        grammar_length = self.get_grammar_length(parsing_grammar)
        input_length = self.get_input_length(parsing_grammar, parsing_results)
        if log:
            self.log("Grammar: %s" % (grammar_length, ))
            self.log("Input: %s" % (input_length, ))
        
        return grammar_length + input_length
        
    def get_parsing_results(self, hypothesis, deleted = None, added = None, flipped_word = None):
        self.new_parsing_dict = {}
        parsing_results = []
        
        self.last_print_time = time.time()
        
        for i, sentence in enumerate(self.input):
            # If the deleted item didn't take part in the derivation then we don't need to parse again.
            if deleted is not None:
                previous_composing_items = self.input_parsing_dict[sentence][0].composing_items
                previous_composing_items_str = [str(item) for item in list(previous_composing_items)]
                if str(deleted) not in previous_composing_items_str:
                    parsing_results.append(self.input_parsing_dict[sentence])
                    self.new_parsing_dict[sentence] = self.input_parsing_dict[sentence]
                    continue
                
            # If the added item isn't a word in the sentence then we don't need to parse again.
            if added is not None and added.head.substring not in sentence.split():
                parsing_results.append(self.input_parsing_dict[sentence])
                self.new_parsing_dict[sentence] = self.input_parsing_dict[sentence]
                continue
                
            if flipped_word is not None and flipped_word not in sentence.split():
                parsing_results.append(self.input_parsing_dict[sentence])
                self.new_parsing_dict[sentence] = self.input_parsing_dict[sentence]
                continue
            
            parser = NumberBottomUpParser(hypothesis)
            result = parser.parse(sentence)
            
            if not result:
                raise AnnealerException("Current hypothesis doesn't parse input! Failed on \"%s\"" % (sentence, ))
            
            results = parser.results
            parsing_results.append(results)
            self.new_parsing_dict[sentence] = results
            
            if time.time() - self.last_print_time > 10:
                print("Parsed %d sentences - (%s seconds since last update)" % (i + 1, time.time() - self.last_print_time))
                self.last_print_time = time.time()
        
        return parsing_results
        
    def ceil_log_base_2(self, number):
        if number == 0:
            return 0
        if number == 1:
            return 1
        return int(math.ceil(math.log(number, 2)))
        
    def get_grammar_length(self, hypothesis):
        # We will encode thus:
        # Each word in the 'alphabet' that appears in some grammar item's substring, including the empty string, will get a fixed length code h.
        # Each base will get a fixed length code b.
        # Each licensor will get a fixed length code L.
        # We start by 0*h + 1 + 0*b + 1 + 0*L + 1.
        # Now each tree in the lexicon will be represented in the following way - for each node:
        #   Each word in its head and then the empty string (h * (number_of_words_in_the_head + 1)).
        #   Its base (length b) - only the first node has a base.
        #   For every select - 00 + base (length b).
        #   For every licensor - 01 + licensor (length L).
        #   For every licensee - 10 + licensee (length L).
        #   11 + (0 for another node or 1 for the last node).
        #   0 for s, 1 for c.
        # At the end of each tree - 0 if there are still other trees in the lexicon, 1 if this is the last tree.
        
        total_length = 0
        
        words = self.words + [EMPTY_STRING]
        
        h = self.ceil_log_base_2(len(words))
        b = self.ceil_log_base_2(len(hypothesis.bases))
        L = self.ceil_log_base_2(len(hypothesis.licensors))

        total_length += h + 1 + b + 1 + L + 1
        
        for tree in hypothesis.lexicon:
            tree_length = 0
            for node in tree.nodes:
                # tree_length += h
                if node.substring == EMPTY_STRING:
                    number_of_words_in_substring = 0
                elif self.separator == '':
                    number_of_words_in_substring = len(list(node.substring))
                else:
                    number_of_words_in_substring = len(node.substring.split(self.separator))
                tree_length += h * (number_of_words_in_substring + 1)
                
                if node.base: # This should apply for the first node only.
                    tree_length += b
                    
                tree_length += (2 + b) * len(node.selects)
                licenses = node.licensors + node.licensees
                tree_length += (2 + L) * len(licenses)
                
                tree_length += 3 # The end of the node.
                
                tree_length += 1 # s or c.
                
            tree_length += 1 # Is this the last tree.
                
            total_length += tree_length
            
        # Add the merge direction:
        if self.learner_type == "Kayne":
            # In the Kayne learner there is only one direction and so it should not be encoded.
            pass
        elif self.learner_type == "Language":
            # We add one bit to the grammar to encode the language merge direction.
            total_length += 1
        elif self.learner_type == "Category":
            # We add one bit per category to encode the category merge direction.
            total_length += len(hypothesis.bases)
        elif self.learner_type == "Word":
            # We add one bit per lexical item to encode the word merge direction.
            total_length += len(hypothesis.lexicon)
        else:
            raise AnnealerException("Unexpected learner type - %s" % (self.learner_type, ))
            
        return total_length
        
    def get_input_length(self, hypothesis, parsing_results):
        total = 0
        
        for result in sum(parsing_results, []):
            total += self.get_sentence_length(hypothesis, result)
            
        return total
        
    def get_sentence_length(self, hypothesis, result):
        # We will encode the input thus:
        # We calculate the derivation of the parsing and get the number of steps.
        # We enumerate the trees in the lexicon and the steps of the derivation and assign a fixed length code for each - k.
        # We start by 0*k + 1.
        # We encode the input by steps of the derivation:
        #   0 for merge or 1 for move.
        #   For merge - we also write the two trees that were merged (either from the lexicon or results of previous steps in the derivation).
        #   For move - we write the tree that moved (either from the lexicon or a result of a previous step in the derivation).
        # We write the derivation step that produced the input sentence (usually the last one) - k.
        
        k = self.ceil_log_base_2(len(hypothesis.lexicon) + result.derivation_length)
        
        # 0*k + 1
        total_length = k + 1
        
        # Number of 1's in derivation steps.
        total_length += result.derivation_length
        # Length of all items in derivation steps
        total_length += result.derivation_size * k
        
        # The derivation step that produced the input sentence.
        total_length += k
        
        return total_length

if __name__ == '__main__':
    from minimalist_grammar.MinimalistGrammar import get_grammar_from_string
    
    input = ["John fell", "Paul fell", "George fell", "Ringo fell"]
    print(input)
    
    grammar_string_1 = "[[>@: IP]s, [>John: IP =IP]s, [>Paul: IP =IP]s, [>George: IP =IP]s, [>Ringo: IP =IP]s, [>fell: IP =IP]s]"#, [>in: IP =IP]s, [>love: IP =IP]s]"
    print(grammar_string_1)
    grammar_string_2 = "[%s]" % (", ".join(["[>%s: IP]s" % (blb, ) for blb in input]), )
    print(grammar_string_2)
    grammar_string_3 = "[[>@: IP =VP =DP]s, [>John: DP]s, [>Paul: DP]s, [>George: DP]s, [>Ringo: DP]s, [>fell: VP]s]"
    print(grammar_string_3)

    grammar_1 = get_grammar_from_string(grammar_string_1)
    grammar_2 = get_grammar_from_string(grammar_string_2)
    grammar_3 = get_grammar_from_string(grammar_string_3)
    
    from BlankGrammars import *
    def log(x):
        print(x)
    annealer = MinimalistGrammarAnnealer(input, KAYNE_GRAMMAR_WITH_HACK, "Kayne", log)
    
    energy = annealer.energy(grammar_1)
    print("Energy 1:", energy)
    energy = annealer.energy(grammar_2)
    print("Energy 2:", energy)
    energy = annealer.energy(grammar_3)
    print("Energy 3:", energy)
