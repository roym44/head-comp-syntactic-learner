import time
import pprint

from Grammars import *
from MinimalistGrammarTree import *
from MinimalistGrammar import get_grammar_from_string


class BottomUpParser(object):

    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, input):
        self.init_chart()
        self.init_agenda(input)
        self.init_goals(input)

        while self.agenda:
            trigger = self.agenda.pop()

            if trigger.size() > len(input):
                continue
            if trigger not in self.chart:
                self.chart.append(trigger)

                moved = trigger.move()
                if moved and moved.is_possible_for_input(input):
                    self.agenda.append(moved)

                for item in self.chart:
                    merged = trigger.merge(item)
                    if merged and merged.is_possible_for_input(input):
                        self.agenda.append(merged)
                    merged = item.merge(trigger)
                    if merged and merged.is_possible_for_input(input):
                        self.agenda.append(merged)

        self.results = []
        for item in self.chart:
            if str(item) in self.goals:
                self.results.append(item)

        if self.results:
            return True
        return False

    def init_chart(self):
        self.chart = []

    def init_agenda(self, input):
        self.agenda = []
        input_substrings = self.split_input(input)
        for item in self.grammar.lexicon:
            if item.head.substring in input or item.head.substring == EMPTY_STRING:
                self.agenda.append(item)

    def split_input(self, input):
        if SUBSTRING_DELIMITER == '':
            # This means we treat letters as words.
            return list(input)
        return input.split(SUBSTRING_DELIMITER)

    def init_goals(self, input):
        self.goals = ["[>%s: IP]s" % (input,),
                      "[>%s: IP]c" % (input,),
                      "[<%s: IP]s" % (input,),
                      "[<%s: IP]c" % (input,)]


def parse_sentence(grammar, sentence, draw_tree=False):
    parser = BottomUpParser(grammar)

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
        print("Derivation:")  # item.derivation
        pprint.pprint(item.derivation)
        print("")
        if draw_tree:
            from ParseTreePrinter import print_parse_tree
            print_parse_tree(sentence, item.nested_derivation)
        # print "Nested derivation:", item.nested_derivation

    print("\nElapsed time:", end - start)


if __name__ == '__main__':
    input = "the king knows which wine the queen prefers"
    grammar = STABLER_GRAMMAR
    parse_sentence(grammar, input, True)

    input = "Pikachu library the in Squirtle library the in Pikachu sang that thought that thought"
    input = "Pikachu library the in Squirtle saw"

    grammar_string = "[[@: c =IP]s, [@: IP =VP =DP]s, [runs: VP]s, [walks: VP]s, [reads: VP]s, [writes: VP]s, [likes: V]s, [sees: V]s, [loves: V]s, [hates: V]s, [Jerry: DP]s, [George: DP]s, [Elaine: DP]s, [Kramer: DP]s, [boy: N]s, [girl: N]s, [dog: N]s, [cat: N]s, [a: D]s, [the: D]s, [@: head =V]s, [@: head =P]s, [@: head =C]s, [@: head =D]s, [@: complement =DP]s, [@: complement =DP -kayne]s, [@: complement =N]s, [@: complement =N -kayne]s, [@: complement =IP]s, [@: complement =IP -kayne]s, [@: VP =complement =head]s, [@: VP =complement =head +kayne]s, [@: PP =complement =head]s, [@: PP =complement =head +kayne]s, [@: CP =complement =head]s, [@: CP =complement =head +kayne]s, [@: DP =complement =head]s, [@: DP =complement =head +kayne]s]"
    grammar = get_grammar_from_string(grammar_string)
    input = ['Kramer walks', 'Kramer runs', 'George reads', 'Kramer runs', 'Elaine runs', 'Elaine runs', 'George runs',
             'Kramer walks', 'Elaine writes', 'Jerry reads', 'George reads', 'Elaine runs', 'Elaine writes',
             'George walks', 'Elaine reads', 'George walks', 'Kramer reads', 'Jerry writes', 'Kramer writes',
             'George runs', 'Jerry walks', 'Elaine walks', 'George walks', 'Jerry runs', 'Elaine walks',
             'Elaine writes', 'Jerry walks', 'Jerry runs', 'Elaine reads', 'Jerry walks', 'Elaine runs', 'George reads',
             'George reads', 'Elaine writes', 'George walks', 'Jerry writes', 'Jerry reads', 'Jerry walks',
             'Kramer walks', 'Elaine writes', 'Elaine writes', 'George walks', 'Kramer runs', 'Elaine walks',
             'Jerry walks', 'George writes', 'Elaine runs', 'Jerry runs', 'George walks', 'Jerry runs']
    sentence = "Kramer sees a boy"
