import random
from typing import Tuple, Optional

from minimalist_grammar.MinimalistGrammar import *
from learner import MinimalistGrammarAnnealer

ADD_CHAR_PROB = 0.02
REMOVE_CHAR_PROB = 0.02
MUTATE_CHAR_PROB = 0.1


class MGGA(object):
    def __init__(self, mg_annealer: MinimalistGrammarAnnealer):
        self.mga = mg_annealer

    def generate_individual_grammar(self) -> Tuple[MinimalistGrammar, float]:
        genotype = self.mga.get_initial_hypothesis()
        fitness = self.evaluate_fitness_grammar(genotype, None)
        return genotype, fitness

    def evaluate_fitness_grammar(self, genotype: MinimalistGrammar, target: Optional[str]) -> float:
        fitness = self.mga.energy(genotype)
        self.mga.initial_input_parsing_dict = self.mga.new_parsing_dict
        return fitness

    def mutate_grammar(self, genotype: MinimalistGrammar, target: Optional[str]) -> MinimalistGrammar:
        new_hypothesis, new_energy = self.mga.random_neighbour(genotype)
        return new_hypothesis

    def crossover_grammar(self, parent1: MinimalistGrammar, parent2: MinimalistGrammar,
                          target: Optional[str]) -> Tuple[MinimalistGrammar, MinimalistGrammar]:
        return parent1, parent2
