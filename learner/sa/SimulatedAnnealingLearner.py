import math
import time

from learner.sa.MinimalistGrammarAnnealer import MinimalistGrammarAnnealer
from input.InputGenerator import *


class SimulatedAnnealingLearner(object):

    def __init__(self, logger, annealer: MinimalistGrammarAnnealer, initial_temperature, initial_hypothesis=None):
        self.logger = logger
        self.annealer = annealer
        self.hypothesis = initial_hypothesis if initial_hypothesis else self.annealer.get_initial_hypothesis()
        self.logger.info(f"Initial hypothesis: {self.hypothesis}")
        self.temperature = initial_temperature
        self.current_energy = None
        self.iteration = 0
        self.total_time = 0

    def anneal(self, steps):
        start = time.time()
        total_steps = self.iteration + steps
        self.current_energy = self.annealer.energy(self.hypothesis)
        self.annealer.initial_input_parsing_dict = self.annealer.new_parsing_dict
        for i in range(steps):
            self.logger.info(f"\nIteration: {self.iteration}")
            print(f"Time: {time.strftime('%Y_%m_%d__%H_%M_%S: ')}")
            self.logger.info(f"Hypothesis: {self.hypothesis}")
            self.logger.info(f"Energy: {self.current_energy}")
            self.logger.info(f"Temperature: {self.temperature}")

            # I made the neighbour function also calculate the energy to save time.
            new_hypothesis, new_energy = self.annealer.random_neighbour(self.hypothesis)
            if new_hypothesis is not None:
                self.logger.info(f"New Energy: {new_energy}")
                delta = new_energy - self.current_energy
                self.logger.info(f"Delta: {delta}")
                if delta <= 0:
                    p = 1
                else:
                    p = math.e ** (0 - (delta / self.temperature))
                self.logger.info(f"Change probability: {p}")
                if random.random() < p and self.hypothesis != new_hypothesis:
                    self.hypothesis = new_hypothesis
                    self.current_energy = new_energy
                    self.annealer.initial_input_parsing_dict = self.annealer.new_parsing_dict
                    self.logger.info("Changed hypotheses.")
                else:
                    self.logger.info("Didn't change hypotheses.")
            else:
                self.logger.info("Didn't change hypotheses.")

            self.temperature = 0.997 * self.temperature
            self.iteration += 1

            if self.temperature < 0.5:
                break

        elapsed = time.time() - start
        self.total_time += elapsed

        self.logger.info(f"\nIteration: {self.iteration}\nHypothesis: {self.hypothesis}\nEnergy: {self.current_energy}\n"
                         f"Temperature: {self.temperature}\nElapsed time: {time.time() - start}")
        return self.iteration, self.hypothesis, self.temperature

