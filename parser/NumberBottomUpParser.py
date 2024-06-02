import time
from itertools import product

from minimalist_grammar.MinimalistGrammar import get_grammar_from_string
from minimalist_grammar.MinimalistGrammarNode import MinimalistGrammarNode
from minimalist_grammar import MinimalistGrammarTree, NumberMinimalistGrammarTree
from minimalist_grammar.NumberMinimalistGrammarNode import NumberMinimalistGrammarNode


class NumberBottomUpParser(object):

    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, input):
        self.init_agenda(input)
        self.init_goals(input)
        self.results = []

        best_result = None

        # For simpler inputs the obvious parsing is quicker.
        if self.input_length < 100:
            self.init_chart()
            results = self.parse_permutation(self.agenda)
            for result in results:
                if best_result is None or \
                        result.derivation_length < best_result.derivation_length or \
                        (
                                result.derivation_length == best_result.derivation_length and result.derivation_size < best_result.derivation_size):
                    best_result = result
        else:
            self.agenda_permutations = self.get_agenda_permutations()
            print("Number of permutations:", len(self.agenda_permutations))
            results = []

            for i, agenda in enumerate(self.agenda_permutations):
                self.init_chart()
                if i % 10 == 0:
                    print("permutation ", i)
                perm_results = self.parse_permutation(agenda, None)
                for result in perm_results:
                    if best_result is None or \
                            result.derivation_length < best_result.derivation_length or \
                            (
                                    result.derivation_length == best_result.derivation_length and result.derivation_size < best_result.derivation_size):
                        best_result = result
                results += perm_results

        if best_result is not None:
            self.results = [best_result]

        if self.results:
            self.translate_result_composing_items()
            return True
        return False

    def translate_result_composing_items(self):
        for result in self.results:
            new_items = set([])
            for item in result.composing_items:
                new_items |= {self.translate_to_strings(item)}
            result.composing_items = new_items

    # This tries to make the parser more efficient by only testing one permutation of categories for the input.
    # If the input has several different possibilities for each word then the parsing will take a long time.
    # Here we split it and hopefully the parsing is quicker this way.
    def get_agenda_permutations(self):
        permutations = []
        substring_dict = {}

        # Generate dictionary.
        for item in self.agenda:
            if str(item.nodes[0].substring) not in substring_dict:
                substring_dict[str(item.nodes[0].substring)] = [item]
            else:
                substring_dict[str(item.nodes[0].substring)].append(item)

        possible_words = [substring_dict[str(self.substrings[substring])] for substring in self.input_substrings]

        permutations = [substring_dict[str(NumberMinimalistGrammarTree.EMPTY_STRING)] + list(permutation) for
                        permutation in product(*possible_words)]
        return permutations

    def parse_permutation(self, agenda, current_best_result=None):
        results = []

        if current_best_result is None:
            # A merge operation for every word in the input, then up to 3 actions for every connection of two
            # trees (I think two merges and one move should be more than reasonable) and one more merge for the full sentence.
            # max_derivation_length = self.input_length + (self.input_length * 3) + 1
            max_derivation_length = self.input_length + (self.input_length * 2) + 1
        else:
            max_derivation_length = current_best_result.derivation_length

        while agenda:
            trigger = self.get_trigger_item(agenda)

            if max_derivation_length < trigger.derivation_length:
                continue

            if trigger.size() > self.input_length:
                continue

            if trigger not in self.chart:
                self.chart.append(trigger)

                moved = trigger.move()
                if moved and moved not in self.chart:
                    self.append_to_agenda(agenda, moved)
                    if self.is_goal_item(moved):
                        return [moved]

                for item in self.chart:
                    merged = trigger.merge(item)
                    if merged and merged not in self.chart:
                        self.append_to_agenda(agenda, merged)
                        if self.is_goal_item(merged):
                            return [merged]
                    merged = item.merge(trigger)
                    if merged and merged not in self.chart:
                        self.append_to_agenda(agenda, merged)
                        if self.is_goal_item(merged):
                            return [merged]

        for item in self.chart:
            if self.is_goal_item(item):
                results.append(item)

        return results

    # By smartly selecting the trigger we can reduce the running time of the parser.
    def get_trigger_item(self, agenda):
        max_item = agenda[0]
        for item in agenda:
            if sum([j - i for i, j in sum([node.substring for node in item.nodes], [])]) > sum(
                    [j - i for i, j in sum([node.substring for node in max_item.nodes], [])]):
                max_item = item

        agenda.remove(max_item)
        return max_item

    # Since we only return one result, we might as well choose the best possibilities along the way.
    # This makes the parsing slightly faster since we stop working with the less efficient possibilities.
    def append_to_agenda(self, agenda, item):
        if item in agenda:
            existing = agenda[agenda.index(item)]
            if item.derivation_length < existing.derivation_length or \
                    (
                            item.derivation_length == existing.derivation_length and item.derivation_size < existing.derivation_size):
                agenda.remove(existing)
                agenda.append(item)
        else:
            agenda.append(item)

    def init_chart(self):
        self.chart = []

    def init_agenda(self, input):
        self.agenda = []
        self.input_substrings = self.split_substring(input)
        self.input_length = len(self.input_substrings)
        self.init_translation_dicts()
        self.invert_translation_dicts()
        for item in self.grammar.lexicon:
            if item.head.substring == MinimalistGrammarTree.EMPTY_STRING:
                self.agenda.append(self.translate_to_numbers(item, NumberMinimalistGrammarTree.EMPTY_STRING))
            else:
                item_words = self.split_substring(item.head.substring)
                # We want to find all occurrences of the substring in the input and add an item for each.
                for i in range(self.input_length - len(item_words) + 1):
                    found = True
                    for j in range(len(item_words)):
                        if self.input_substrings[i + j] != item_words[j]:
                            found = False
                    if found:
                        self.agenda.append(self.translate_to_numbers(item, [(i, i + len(item_words))]))

    def init_translation_dicts(self):
        self.substrings = {}
        self.categories = {}
        self.licenses = {}

        category_set = set([])
        category_set |= {"IP"}  # It should already be there but if it isn't we add it so the goals work.
        license_set = set([])

        for i, substring in enumerate(self.input_substrings):
            # The same word can appear several times in the same sentence.
            if substring in self.substrings:
                self.substrings[substring].append((i, i + 1))
            else:
                self.substrings[substring] = [(i, i + 1)]
        self.substrings[MinimalistGrammarTree.EMPTY_STRING] = NumberMinimalistGrammarTree.EMPTY_STRING

        for item in self.grammar.lexicon:
            for node in item.nodes:
                category_set |= {node.base}
                category_set |= set(node.selects)
                license_set |= set(node.licensors)
                license_set |= set(node.licensees)

        for i, category in enumerate(category_set):
            self.categories[category] = i

        for i, license in enumerate(license_set):
            self.licenses[license] = i

        self.types = {MinimalistGrammarTree.TYPE_SIMPLE: NumberMinimalistGrammarTree.TYPE_SIMPLE,
                      MinimalistGrammarTree.TYPE_COMPLEX: NumberMinimalistGrammarTree.TYPE_COMPLEX}

    def translate_to_numbers(self, string_tree, substring_in_numbers):
        type = self.types[string_tree.type]
        nodes = []
        for node in string_tree.nodes:
            if node == string_tree.nodes[0]:
                substring = substring_in_numbers
            else:
                substring = self.substrings[node.substring]
            base = self.categories[node.base]
            selects = []
            for select in node.selects:
                selects.append(self.categories[select])
            licensors = []
            for licensor in node.licensors:
                licensors.append(self.licenses[licensor])
            licensees = []
            for licensee in node.licensees:
                licensees.append(self.licenses[licensee])
            nodes.append(NumberMinimalistGrammarNode(substring, base, selects, licensors, licensees))
        new_tree = NumberMinimalistGrammarTree.NumberMinimalistGrammarTree(nodes, type)
        new_tree.complement_merge_direction = string_tree.complement_merge_direction
        return new_tree

    def invert_translation_dicts(self):
        self.inverted_types = {v: k for k, v in self.types.items()}
        self.inverted_categories = {v: k for k, v in self.categories.items()}
        self.inverted_licenses = {v: k for k, v in self.licenses.items()}

    def translate_to_strings(self, number_tree):
        type = self.inverted_types[number_tree.type]
        nodes = []
        for node in number_tree.nodes:
            if node.substring == NumberMinimalistGrammarTree.EMPTY_STRING:
                substring = MinimalistGrammarTree.EMPTY_STRING
            else:
                substring = MinimalistGrammarTree.SUBSTRING_DELIMITER.join(
                    self.input_substrings[node.substring[0][0]: node.substring[0][1]])
            if node.base is None:
                base = node.base
            else:
                base = self.inverted_categories[node.base]
            selects = []
            for select in node.selects:
                selects.append(self.inverted_categories[select])
            licensors = []
            for licensor in node.licensors:
                licensors.append(self.inverted_licenses[licensor])
            licensees = []
            for licensee in node.licensees:
                licensees.append(self.inverted_licenses[licensee])
            new_node = MinimalistGrammarNode()
            new_node.substring = substring
            new_node.base = base
            new_node.selects = selects
            new_node.licensors = licensors
            new_node.licensees = licensees
            nodes.append(new_node)
        new_tree = MinimalistGrammarTree.MinimalistGrammarTree()
        new_tree.nodes = nodes
        new_tree.type = type
        new_tree.hash = hash(str(new_tree))
        new_tree.complement_merge_direction = number_tree.complement_merge_direction
        return new_tree

    def split_substring(self, substring):
        if MinimalistGrammarTree.SUBSTRING_DELIMITER == '':
            # This means we treat letters as words.
            return list(substring)
        return substring.split(MinimalistGrammarTree.SUBSTRING_DELIMITER)

    def init_goals(self, input):
        self.goals = [NumberMinimalistGrammarTree.NumberMinimalistGrammarTree([
                                                                                  NumberMinimalistGrammarTree.NumberMinimalistGrammarNode(
                                                                                      [(0, self.input_length)],
                                                                                      self.categories["IP"], [], [],
                                                                                      [])],
                                                                              NumberMinimalistGrammarTree.TYPE_SIMPLE,
                                                                              "right"),
                      NumberMinimalistGrammarTree.NumberMinimalistGrammarTree([
                                                                                  NumberMinimalistGrammarTree.NumberMinimalistGrammarNode(
                                                                                      [(0, self.input_length)],
                                                                                      self.categories["IP"], [], [],
                                                                                      [])],
                                                                              NumberMinimalistGrammarTree.TYPE_COMPLEX,
                                                                              "right"),
                      NumberMinimalistGrammarTree.NumberMinimalistGrammarTree([
                                                                                  NumberMinimalistGrammarTree.NumberMinimalistGrammarNode(
                                                                                      [(0, self.input_length)],
                                                                                      self.categories["IP"], [], [],
                                                                                      [])],
                                                                              NumberMinimalistGrammarTree.TYPE_SIMPLE,
                                                                              "left"),
                      NumberMinimalistGrammarTree.NumberMinimalistGrammarTree([
                                                                                  NumberMinimalistGrammarTree.NumberMinimalistGrammarNode(
                                                                                      [(0, self.input_length)],
                                                                                      self.categories["IP"], [], [],
                                                                                      [])],
                                                                              NumberMinimalistGrammarTree.TYPE_COMPLEX,
                                                                              "left")]

    # This is a comaprison that ignores type, merge direction and optional licensees.
    def is_goal_item(self, item):
        is_goal = (len(item.nodes) == 1
                   and item.head.substring == [(0, self.input_length)]
                   and item.head.base == self.categories["IP"]
                   and not item.head.selects
                   and not item.head.licensors
                   and not item.head.licensees
                   )
        return is_goal


def parse_sentence(grammar, sentence, draw_tree=False):
    parser = NumberBottomUpParser(grammar)

    print("Parsing the sentence:", sentence)
    print("...")
    start = time.time()
    # try:
    if True:
        result = parser.parse(sentence)
    else:
        # except:
        import pdb;
        pdb.set_trace()

    if result:
        print("The sentence is in my language.")
    else:
        print("The sentence is ungrammatical in my language!")
    end = time.time()

    for item in parser.results:
        print("Item:", item)
        # print "Derivation length:", item.derivation_length
        # print "Derivation size:", item.derivation_size
        if draw_tree:
            from ParseTreePrinter import print_parse_tree
            print_parse_tree(sentence, item.nested_derivation, translation_func=parser.translate_to_strings)

    print("\nElapsed time:", end - start)


def parse_input(grammar, input):
    parser = NumberBottomUpParser(grammar)
    print("Parsing %d sentences" % (len(input),))
    start = time.time()
    for i, sentence in enumerate(input):
        print(i, sentence, "-", end=' ')
        result = parser.parse(sentence)
        print(result)
        if not result:
            print("Failed")
            break
    else:
        print("All sentences are parsed.")
    end = time.time()
    print("\nElapsed time:", end - start)


def compare_hypotheses(input, grammar_1, grammar_2):
    parser_1 = NumberBottomUpParser(grammar_1)
    parser_2 = NumberBottomUpParser(grammar_2)
    print("Parsing %d sentences" % (len(input),))
    start = time.time()
    total_length_1 = 0
    total_length_2 = 0
    total_size_1 = 0
    total_size_2 = 0
    for i, sentence in enumerate(input):
        # print i, sentence, "-",
        result_1 = parser_1.parse(sentence)
        result_2 = parser_2.parse(sentence)
        if not result_1 or not result_2:
            if not result_1:
                print(i, sentence, "-", "Failed to parse by grammar 1")
            if not result_2:
                print(i, sentence, "-", "Failed to parse by grammar 2")
            continue
        length_1 = parser_1.results[0].derivation_length
        length_2 = parser_2.results[0].derivation_length
        size_1 = parser_1.results[0].derivation_size
        size_2 = parser_2.results[0].derivation_size
        if length_1 != length_2 or size_1 != size_2:
            print(i, sentence, "-", "Different:")
            print("Length 1 -", length_1, "Size 1:", size_1)
            print("Length 2 -", length_2, "Size 2:", size_2)
        else:
            print(i, sentence, "-", "Same")
        total_length_1 += length_1
        total_length_2 += length_2
        total_size_1 += size_1
        total_size_2 += size_2
    end = time.time()
    print("\nElapsed time:", end - start)
    print("Grammar 1: length -", len(grammar_1.lexicon), "total input length -", total_length_1, "total input size -",
          total_size_1)
    print("Grammar 2: length -", len(grammar_2.lexicon), "total input length -", total_length_2, "total input size -",
          total_size_2)


if __name__ == '__main__':
    NumberMinimalistGrammarTree.WITH_NESTED_DERIVATION = True

    input = ['George wrote Kramer and Kramer above', 'Jerry and Elaine Jerry loved',
             'George walked and Elaine read Elaine with',
             'Elaine Jerry saw Jerry by and Jerry Elaine hated Jerry under',
             'Jerry Elaine read that knows and Jerry Kramer hated', 'George and Jerry read', 'Kramer read',
             'Kramer walked Kramer with', 'Elaine walked and Kramer Jerry liked Jerry by',
             'George George ran that thinks and walked', 'Elaine read', 'George wrote George and Kramer with',
             'Jerry wrote Jerry and George with', 'George read and Kramer Elaine loved',
             'Elaine read and Elaine Kramer wrote that assumes Elaine above',
             'Elaine Jerry Jerry liked George under that says and ran', 'George read and Elaine read',
             'Jerry ran and Kramer wrote Elaine by',
             'Kramer Elaine walked that says and Kramer George Elaine saw that assumes Kramer above',
             'George wrote and walked', 'Jerry George and George walked that says George under',
             'Elaine and Elaine wrote', 'George ran', 'Jerry and Jerry walked', 'Kramer and Elaine ran George under',
             'George George loved George above and George ran', 'Elaine and Kramer Kramer saw', 'Kramer ran',
             'Kramer read and Jerry loved', 'Jerry ran and Jerry wrote Kramer by', 'Jerry and Kramer read',
             'Kramer walked Jerry with', 'Jerry wrote Elaine and George with',
             'George Kramer George liked that thinks and George Kramer hated',
             'Jerry George saw Elaine above and Kramer under', 'Jerry ran George and Kramer under',
             'Kramer Jerry Kramer liked that assumes', 'Jerry Elaine hated and Kramer read',
             'Elaine and Kramer George saw', 'Jerry Jerry and Kramer liked', 'Kramer walked and Jerry Jerry liked',
             'George and Elaine read', 'Elaine ran and wrote Jerry under', 'Elaine read',
             'George walked and George Elaine loved George with', 'Elaine wrote', 'Jerry wrote and Kramer saw',
             'Elaine wrote and Elaine liked', 'Jerry and Kramer ran', 'Elaine Kramer liked']

    grammar_string = "[[>@: IP =VP =DP]s, [>@: VP =PP =VP]s, [>@: DP =DP -O]s, [>@: IP =IP -Comp]s, [>hated: VP =DP]s, [>read: VP =DP]s, [>above: VP =DP]s, [>saw: VP =DP]s, [>walked: VP =DP]s, [>assumed: VP =DP]s, [>that: VP =DP]s, [>ran: VP =DP]s, [>said: VP =DP]s, [>thought: VP =DP]s, [>George: VP =CP]s, [>loved: VP =CP]s, [>Jerry: VP =CP]s, [>Elaine: VP =CP]s, [>and: VP =CP]s, [>with: VP =CP]s, [>wrote: VP =CP]s, [>by: VP =CP]s, [>Kramer: VP =CP]s, [>under: VP =CP]s, [>liked: VP =CP]s, [>hated: VP =CP]s, [>saw: VP =CP]s, [>walked: VP =CP]s, [>assumed: VP =CP]s, [>that: VP =CP]s, [>ran: VP =CP]s, [>said: VP =CP]s, [>thought: VP =CP]s, [>George: PP =DP]s, [>loved: PP =DP]s, [>Jerry: PP =DP]s, [>Elaine: PP =DP]s, [>and: PP =DP]s, [>with: PP =DP]s, [>wrote: PP =DP]s, [>by: PP =DP]s, [>Kramer: PP =DP]s, [>under: PP =DP]s, [>liked: PP =DP]s, [>hated: PP =DP]s, [>read: PP =DP]s, [>above: PP =DP]s, [>saw: PP =DP]s, [>walked: PP =DP]s, [>assumed: PP =DP]s, [>that: PP =DP]s, [>ran: PP =DP]s, [>said: PP =DP]s, [>thought: PP =DP]s, [>George: CP =IP +Comp -Oc]s, [>loved: CP =IP +Comp -Oc]s, [>Jerry: CP =IP +Comp -Oc]s, [>Elaine: CP =IP +Comp -Oc]s, [>with: CP =IP +Comp -Oc]s, [>and: CP =IP +Comp -Oc]s, [>wrote: CP =IP +Comp -Oc]s, [>by: CP =IP +Comp -Oc]s, [>Kramer: CP =IP +Comp -Oc]s, [>under: CP =IP +Comp -Oc]s, [>liked: CP =IP +Comp -Oc]s, [>hated: CP =IP +Comp -Oc]s, [>read: CP =IP +Comp -Oc]s, [>above: CP =IP +Comp -Oc]s, [>saw: CP =IP +Comp -Oc]s, [>walked: CP =IP +Comp -Oc]s, [>assumed: CP =IP +Comp -Oc]s, [>that: CP =IP +Comp -Oc]s, [>ran: CP =IP +Comp -Oc]s, [>said: CP =IP +Comp -Oc]s, [>thought: CP =IP +Comp -Oc]s, [>George: VP =DP +O]s, [>loved: VP =DP +O]s, [>Jerry: VP =DP +O]s, [>Elaine: VP =DP +O]s, [>and: VP =DP +O]s, [>with: VP =DP +O]s, [>wrote: VP =DP +O]s, [>by: VP =DP +O]s, [>Kramer: VP =DP +O]s, [>under: VP =DP +O]s, [>liked: VP =DP +O]s, [>hated: VP =DP +O]s, [>read: VP =DP +O]s, [>above: VP =DP +O]s, [>saw: VP =DP +O]s, [>walked: VP =DP +O]s, [>assumed: VP =DP +O]s, [>that: VP =DP +O]s, [>ran: VP =DP +O]s, [>said: VP =DP +O]s, [>thought: VP =DP +O]s, [>George: VP =CP +Oc]s, [>loved: VP =CP +Oc]s, [>Jerry: VP =CP +Oc]s, [>Elaine: VP =CP +Oc]s, [>and: VP =CP +Oc]s, [>with: VP =CP +Oc]s, [>wrote: VP =CP +Oc]s, [>by: VP =CP +Oc]s, [>Kramer: VP =CP +Oc]s, [>under: VP =CP +Oc]s, [>liked: VP =CP +Oc]s, [>hated: VP =CP +Oc]s, [>read: VP =CP +Oc]s, [>above: VP =CP +Oc]s, [>saw: VP =CP +Oc]s, [>walked: VP =CP +Oc]s, [>assumed: VP =CP +Oc]s, [>that: VP =CP +Oc]s, [>ran: VP =CP +Oc]s, [>said: VP =CP +Oc]s, [>thought: VP =CP +Oc]s, [>loved: PP =DP +O]s, [>George: PP =DP +O]s, [>Jerry: PP =DP +O]s, [>Elaine: PP =DP +O]s, [>and: PP =DP +O]s, [>with: PP =DP +O]s, [>wrote: PP =DP +O]s, [>by: PP =DP +O]s, [>Kramer: PP =DP +O]s, [>under: PP =DP +O]s, [>liked: PP =DP +O]s, [>hated: PP =DP +O]s, [>read: PP =DP +O]s, [>above: PP =DP +O]s, [>saw: PP =DP +O]s, [>walked: PP =DP +O]s, [>assumed: PP =DP +O]s, [>that: PP =DP +O]s, [>ran: PP =DP +O]s, [>said: PP =DP +O]s, [>thought: PP =DP +O]s, [>George: DP =DP =DP]s, [>loved: DP =DP =DP]s, [>Jerry: DP =DP =DP]s, [>Elaine: DP =DP =DP]s, [>and: DP =DP =DP]s, [>with: DP =DP =DP]s, [>wrote: DP =DP =DP]s, [>by: DP =DP =DP]s, [>Kramer: DP =DP =DP]s, [>under: DP =DP =DP]s, [>liked: DP =DP =DP]s, [>hated: DP =DP =DP]s, [>read: DP =DP =DP]s, [>above: DP =DP =DP]s, [>saw: DP =DP =DP]s, [>walked: DP =DP =DP]s, [>assumed: DP =DP =DP]s, [>that: DP =DP =DP]s, [>ran: DP =DP =DP]s, [>said: DP =DP =DP]s, [>thought: DP =DP =DP]s, [>above: VP =CP]s, [>read: VP =CP]s, [>George: VP]s, [>loved: VP]s, [>Jerry: VP]s, [>Elaine: VP]s, [>and: VP]s, [>with: VP]s, [>wrote: VP]s, [>by: VP]s, [>Kramer: VP]s, [>under: VP]s, [>liked: VP]s, [>hated: VP]s, [>read: VP]s, [>above: VP]s, [>saw: VP]s, [>walked: VP]s, [>assumed: VP]s, [>that: VP]s, [>ran: VP]s, [>said: VP]s, [>thought: VP]s, [>George: DP]s, [>loved: DP]s, [>Jerry: DP]s, [>Elaine: DP]s, [>and: DP]s, [>with: DP]s, [>wrote: DP]s, [>by: DP]s, [>Kramer: DP]s, [>under: DP]s, [>liked: DP]s, [>hated: DP]s, [>read: DP]s, [>above: DP]s, [>saw: DP]s, [>walked: DP]s, [>assumed: DP]s, [>that: DP]s, [>ran: DP]s, [>said: DP]s, [>thought: DP]s, [>George: CP =IP]s, [>loved: CP =IP]s, [>Jerry: CP =IP]s, [>Elaine: CP =IP]s, [>and: CP =IP]s, [>with: CP =IP]s, [>wrote: CP =IP]s, [>by: CP =IP]s, [>Kramer: CP =IP]s, [>under: CP =IP]s, [>liked: CP =IP]s, [>hated: CP =IP]s, [>read: CP =IP]s, [>above: CP =IP]s, [>saw: CP =IP]s, [>walked: CP =IP]s, [>assumed: CP =IP]s, [>that: CP =IP]s, [>ran: CP =IP]s, [>said: CP =IP]s, [>thought: CP =IP]s, [>George: VP =DP]s, [>loved: VP =DP]s, [>Jerry: VP =DP]s, [>Elaine: VP =DP]s, [>and: VP =DP]s, [>with: VP =DP]s, [>wrote: VP =DP]s, [>by: VP =DP]s, [>Kramer: VP =DP]s, [>under: VP =DP]s, [>liked: VP =DP]s]"
    grammar = get_grammar_from_string(grammar_string)
    sentence = "Elaine liked George above Jerry and Kramer"
    parse_sentence(grammar, sentence, draw_tree=True)
