import random
from typing import Tuple, Optional
from minimalist_grammar.MinimalistGrammar import *
from learner.experiment.MinimalistGrammarAnnealer import MinimalistGrammarAnnealer
from learner.ga.ga import GenomeType

MUTATION_RATE = 1


class MGGA(object):
    def __init__(self, mg_annealer: MinimalistGrammarAnnealer):
        self.mga = mg_annealer

    def generate_individual_grammar(self) -> GenomeType:
        # TODO: currently always returns the same initial hypothesis (consider random generation)
        genotype = self.mga.get_initial_hypothesis()
        fitness = self.evaluate_fitness_grammar(genotype, None)
        return genotype, fitness

    def evaluate_fitness_grammar(self, genotype: MinimalistGrammar, target: Optional[MinimalistGrammar]) -> float:
        try:
            fitness = self.mga.energy(genotype)
        except Exception as e:
            print(f"evaluate_fitness_grammar(): energy error {e}")
            return float('inf')  # TODO: a different handling of invalid hypotheses?

        self.mga.initial_input_parsing_dict = self.mga.new_parsing_dict
        return fitness

    def mutate_grammar(self, genotype: MinimalistGrammar, target: Optional[MinimalistGrammar],
                       mutation_rate=MUTATION_RATE) -> GenomeType:
        if random.random() > mutation_rate:
            return genotype, self.evaluate_fitness_grammar(genotype, target)

        new_hypothesis, new_energy = self.mga.random_neighbour(genotype)
        if new_hypothesis is None:
            new_hypothesis = genotype
            new_energy = float('inf')
        # print("mutate_grammar(): new_energy", new_energy)
        return new_hypothesis, new_energy

    def crossover_grammar(self, parent1: MinimalistGrammar, parent2: MinimalistGrammar,
                          target: Optional[MinimalistGrammar]) -> Tuple[MinimalistGrammar, MinimalistGrammar]:
        # TODO: implement crossover
        return parent1, parent2
