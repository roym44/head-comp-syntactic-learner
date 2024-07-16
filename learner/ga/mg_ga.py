import random
import math
from typing import Tuple, Optional
from minimalist_grammar.MinimalistGrammar import *
from learner.experiment.MinimalistGrammarAnnealer import MinimalistGrammarAnnealer
from learner.ga.ga import GenomeType

CROSSOVER_RATE = 0
MUTATION_RATE = 0.9

"""
Note: this object is wrapping an annealer, while in fact it is used in the GA for multiple MGs (population).
This can cause some weird behaviour, I tried an alternative implementation of a MGGAs population instead,
but not in the current version if the project.
    - I saw that the fitness is not well balanced in the population, individual 0 had the best fitness value,
    while the rest had a value with a difference of more that ~500 that didn't go down
    - Also, MGA's random_neighbour() function, added 10 times delete() operation when lexicon size > 70.
    I saw this trend where the lexicon size reached 70, but the fitness was far from 3912 (5.1.1 target) of course,
    but then convergence was really held back, contrary to what I am used to witness in the current implmentation.
    I am still not sure why a population of MGGAs instead of MGs would cause that convergence to stop.
That is why we can't save a field of 'fitness' for example, because this class is not linked directly
to a specific MG, but the annealing process of several of them.
"""


class MGGA(object):
    def __init__(self, logger, mg_annealer: MinimalistGrammarAnnealer):
        self.logger = logger
        self.mga = mg_annealer

    def generate_individual_grammar(self) -> GenomeType:
        # TODO: currently always returns the same initial hypothesis (consider random generation)
        genotype = self.mga.get_initial_hypothesis()
        # only in the beginning here it's okay to calculate the energy
        fitness = self.evaluate_fitness_grammar(genotype, None)
        return genotype, fitness

    def evaluate_fitness_grammar(self, genotype: MinimalistGrammar, target: Optional) -> float:
        try:
            # first time it's okay if genotype.parsing_dict is empty, the flags when calling
            # get_parsing_results_ga() will be False also
            fitness = self.mga.energy(genotype)
            # self.mga.initial_input_parsing_dict = self.mga.new_parsing_dict
        except Exception as e:
            self.logger.error(f"evaluate_fitness_grammar(): energy error = {e}")
            fitness = float('inf')  # TODO: a different handling of invalid hypotheses?
        return fitness

    def mutate_grammar(self, genotype: MinimalistGrammar, previous_fitness: Optional,
                       mutation_rate=MUTATION_RATE) -> GenomeType:
        self.logger.info(f"mutate_grammar(): entered with genotype = {genotype}")
        # don't perform mutation if the probability is too low (p < 1 - mutation_rate)
        if random.random() > mutation_rate:
            self.logger.info("mutate_grammar(): no mutation")
            # TODO: before, I called evaluate_fitness_grammar() here and it caused an exception (cannot parse)!
            return genotype, previous_fitness

        new_hypothesis, new_energy = self.mga.random_neighbour(genotype)
        # hypothesis is invalid, in which case we return the original genotype
        if new_hypothesis is None:
            self.logger.info("mutate_grammar(): new_hypothesis from random neighbour is None")
            return genotype, previous_fitness

        # new_hypothesis.parsing_dict = genotype.parsing_dict.copy()
        # self.mga.initial_input_parsing_dict = self.mga.new_parsing_dict
        self.logger.info("mutate_grammar(): returning new_hypothesis, new_energy")
        return new_hypothesis, new_energy

    def crossover_grammar(self, parent1: MinimalistGrammar, parent2: MinimalistGrammar,
                          target: Optional, crossover_rate=CROSSOVER_RATE) \
            -> Tuple[MinimalistGrammar, MinimalistGrammar]:
        self.logger.info(f"crossover_grammar(): entered")
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

        """
        Note! nothing promises that offspring1 and 2 can parse input! so trying to call evaluate_fitness_grammar()
        can lead to an exception (Current hypothesis doesn't parse input!)
        """
        return offspring1, offspring2
