import time
from loguru import logger

from input.InputGenerator import *
from input.BlankGrammars import *
from minimalist_grammar.MinimalistGrammar import get_grammar_from_string
from learner.MinimalistGrammarAnnealer import MinimalistGrammarAnnealer
from learner.sa.SimulatedAnnealingLearner import SimulatedAnnealingLearner

def test_annealing(input):
    input = input[:-1].split("#")
    logger.info("Input is: %s" % (input,))

    annealer = MinimalistGrammarAnnealer(input)
    hyp = annealer.get_initial_hypothesis()
    logger.info("Initial hypothesis: %s" % (hyp,))
    initial_energy = annealer.energy(hyp)
    logger.info("Initial Energy: %d" % (initial_energy,))

    temperature = int(input("Temperature: "))

    learner = SimulatedAnnealingLearner(annealer, input, temperature)
    while True:
        steps = int(input("Steps: "))
        learner.anneal(steps)


def run_learner():
    print("Time: %s" % (time.strftime("%Y_%m_%d__%H_%M_%S: "),))

    # Head initial:
    custom_input = get_custom_text(size=50, with_transitive="initial", with_dp=None, with_prepositions="initial", with_cp=None,
                                   recursion_depth=1)

    # Head final:
    # input = get_custom_text(size = 50, with_transitive = "final", with_dp = None, with_prepositions = "final", with_cp = "final", recursion_depth = 1)

    # Variation by category:
    # input = get_custom_text(size = 50, with_transitive = "initial", with_dp = None, with_prepositions = "final", with_cp = "initial", recursion_depth = 1)

    # Variation by word:
    # input = get_custom_text(size = 50, with_transitive = "mixed", with_dp = None, with_prepositions = "mixed", with_cp = "mixed", recursion_depth = 1)

    # blank_grammar = KAYNE_GRAMMAR
    # TODO: some valid grammar, "KAYNE_GRAMMAR" doesn't exist
    blank_grammar = KAYNE_GRAMMAR_WITH_EMPTY_DP

    custom_input = custom_input[:-1].split("#")
    logger.info("Input is: %s" % (custom_input,))

    annealer = MinimalistGrammarAnnealer(logger, custom_input, blank_grammar, "Kayne")

    temperature = 1000
    logger.info("Initial Temperature: %f" % (temperature,))

    learner = SimulatedAnnealingLearner(annealer, custom_input, temperature)
    while True:
        custom_input = input("Steps: ")
        if custom_input == 'd':
            import pdb;
            pdb.set_trace()
        steps = int(custom_input)
        learner.anneal(steps)


def test_minimalist_grammar_annealer():
    input = ["John fell", "Paul fell", "George fell", "Ringo fell"]
    print(input)

    grammar_string_1 = "[[>@: IP]s, [>John: IP =IP]s, [>Paul: IP =IP]s, [>George: IP =IP]s, [>Ringo: IP =IP]s, [>fell: IP =IP]s]"  # , [>in: IP =IP]s, [>love: IP =IP]s]"
    print(grammar_string_1)
    grammar_string_2 = "[%s]" % (", ".join(["[>%s: IP]s" % (blb,) for blb in input]),)
    print(grammar_string_2)
    grammar_string_3 = "[[>@: IP =VP =DP]s, [>John: DP]s, [>Paul: DP]s, [>George: DP]s, [>Ringo: DP]s, [>fell: VP]s]"
    print(grammar_string_3)

    grammar_1 = get_grammar_from_string(grammar_string_1)
    grammar_2 = get_grammar_from_string(grammar_string_2)
    grammar_3 = get_grammar_from_string(grammar_string_3)

    annealer = MinimalistGrammarAnnealer(logger, input, KAYNE_GRAMMAR_WITH_HACK, "Kayne")

    energy = annealer.energy(grammar_1)
    print("Energy 1:", energy)
    energy = annealer.energy(grammar_2)
    print("Energy 2:", energy)
    energy = annealer.energy(grammar_3)
    print("Energy 3:", energy)