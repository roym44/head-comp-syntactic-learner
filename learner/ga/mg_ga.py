import random
from copy import deepcopy
from typing import Tuple, Optional

from minimalist_grammar.MinimalistGrammar import *
from learner.MinimalistGrammarAnnealer import MinimalistGrammarAnnealer

ADD_CHAR_PROB = 0.02
REMOVE_CHAR_PROB = 0.02
MUTATE_CHAR_PROB = 0.1


class MGGA(object):
    def __init__(self, mg_annealer: MinimalistGrammarAnnealer):
        self.mga = mg_annealer
        self.indi = (None, 0)
        self.init = False

    def generate_individual_grammar(self) -> Tuple[MinimalistGrammar, float]:
        if self.indi is not (None, 0):
            return deepcopy(self.indi)

        # TODO: currently always returns the same initial hypothesis (not random generation)
        genotype = self.mga.get_initial_hypothesis()
        fitness = self.evaluate_fitness_grammar(genotype, None)
        self.indi = (genotype, fitness)
        return genotype, fitness

    def evaluate_fitness_grammar(self, genotype: MinimalistGrammar, target: Optional[str]) -> float:
        try:
            fitness = self.mga.energy(genotype)
        except Exception as e:
            self.logger.info(f"evaluate_fitness_grammar(): energy error {e}")
            return float('inf')

        self.mga.initial_input_parsing_dict = self.mga.new_parsing_dict
        return fitness

    def mutate_grammar(self, genotype: MinimalistGrammar, target: Optional[str]) -> MinimalistGrammar:
        new_hypothesis, new_energy = self.mga.random_neighbour(genotype)
        return new_hypothesis

    def crossover_grammar(self, parent1: MinimalistGrammar, parent2: MinimalistGrammar,
                          target: Optional[str]) -> Tuple[MinimalistGrammar, MinimalistGrammar]:
        return parent1, parent2
