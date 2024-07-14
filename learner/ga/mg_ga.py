import random
import math
from typing import Tuple, Optional
from minimalist_grammar.MinimalistGrammar import *
from learner.experiment.MinimalistGrammarAnnealer import MinimalistGrammarAnnealer
from learner.ga.ga import GenomeType

CROSSOVER_RATE = 0
MUTATION_RATE = 0.9


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
        # don't perform mutation if the probability is too low (p < 1 - mutation_rate)
        if random.random() > mutation_rate:
            return genotype, self.evaluate_fitness_grammar(genotype, target)

        new_hypothesis, new_energy = self.mga.random_neighbour(genotype)
        if new_hypothesis is None:
            new_hypothesis = genotype
            new_energy = self.evaluate_fitness_grammar(genotype, target)
        # print("mutate_grammar(): new_energy", new_energy)
        return new_hypothesis, new_energy

    def crossover_grammar(self, parent1: MinimalistGrammar, parent2: MinimalistGrammar,
                          target: Optional[MinimalistGrammar], crossover_rate=CROSSOVER_RATE) \
            -> Tuple[MinimalistGrammar, MinimalistGrammar]:
        # don't perform crossover if the probability is too low (p < 1 - crossover_rate)
        if random.random() > crossover_rate:
            return parent1, parent2

        # Create offspring by unilaterally adding random rules from parent2 to parent1's lexicon
        offspring1_lexicon = parent1.lexicon[:]
        offspring2_lexicon = parent2.lexicon[:]

        # Unilateral lexicon crossover
        # Determine number of rules to add from parent2 to parent1 (number between 1 and 20% of parent2's lexicon)
        num_rules_to_add = random.randint(1, len(parent2.lexicon) // 5)  # Random number of rules to add

        # Randomly select rules from parent2 and add them to parent1's lexicon if not already present
        selected_rules = random.sample(offspring2_lexicon, num_rules_to_add)
        for rule in selected_rules:
            if rule not in offspring1_lexicon:
                offspring1_lexicon.append(rule)

        # create new MinimalistGrammar instances for offspring
        offspring1 = MinimalistGrammar(offspring1_lexicon)
        offspring2 = MinimalistGrammar(offspring2_lexicon)

        return offspring1, offspring2
