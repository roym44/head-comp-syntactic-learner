"""
Taken from https://github.com/matanabudy/simple-genetic-algorithm-varying-lengths/blob/main/ga.py
"""
import random
from typing import List, Tuple, Callable, TypeVar, Generic, Optional

import matplotlib.pyplot as plt
import seaborn as sns

# Define a generic type variable for the individual's type
IndividualType = TypeVar("IndividualType")
ExtraArgType = TypeVar("ExtraArgType")

GenomeType = Tuple[IndividualType, float]
GenerateIndividualType = Callable[[], GenomeType]
FitnessFunctionType = Callable[[IndividualType, Optional[ExtraArgType]], float]
MutateFunctionType = Callable[[IndividualType, Optional[ExtraArgType]], GenomeType]
# Crossover should take two parents and an optional extra argument and return two children
CrossoverFunctionType = Callable[
    [IndividualType, IndividualType, Optional[ExtraArgType]],
    Tuple[IndividualType, IndividualType],
]


class GeneticAlgorithm(Generic[IndividualType, ExtraArgType]):
    def __init__(
            self,
            logger,
            fitness_function: FitnessFunctionType[IndividualType, Optional[ExtraArgType]],
            mutate_function: MutateFunctionType[IndividualType, Optional[ExtraArgType]],
            crossover_function: CrossoverFunctionType[IndividualType, Optional[ExtraArgType]],
            generate_individual: Optional[GenerateIndividualType[IndividualType]] = None,
            initial_population: Optional[List[GenomeType]] = None,
            population_size: int = 1000,
            max_generations: int = 1000,
            early_stop_generations: int = 100,
            tournament_size: int = 5,
            extra_arg: Optional[ExtraArgType] = None,
    ):
        if generate_individual is None and initial_population is None:
            raise ValueError("Either generate_individual or initial_population must be provided.")
        if generate_individual is not None and initial_population is not None:
            raise ValueError("Only one of generate_individual or initial_population can be provided.")
        if initial_population is not None and len(initial_population) != population_size:
            raise ValueError("The length of initial_population must be equal to population_size.")

        self.logger = logger
        self.evaluate_fitness = fitness_function
        self.mutate = mutate_function
        self.crossover = crossover_function
        self.population_size = population_size
        self.max_generations = max_generations
        self.early_stop_generations = early_stop_generations
        self.tournament_size = tournament_size
        self.extra_arg = extra_arg
        self.fitness_history: List[float] = []
        self.best_fitness_stagnant_counter = 0
        self.best_individual: Optional[GenomeType] = None
        self.population: List[GenomeType] = [generate_individual() for _ in range(self.population_size)] \
            if generate_individual is not None else initial_population

    @staticmethod
    def selection(population: List[GenomeType], tournament_size: int = 5,
                  num_to_select: Optional[int] = None) -> List[GenomeType]:
        if num_to_select is None:
            num_to_select = len(population)

        selected = []
        for _ in range(num_to_select):
            contenders = random.sample(population, tournament_size)
            selected.append(min(contenders, key=lambda individual: individual[1]))
        return selected

    def evolve(self, elite_size: int = 1) -> None:
        sorted_population = sorted(self.population, key=lambda individual: individual[1])
        elites = sorted_population[:elite_size]
        selected = self.selection(sorted_population[elite_size:], self.tournament_size)
        new_population = elites[:]

        # TODO: no penalty?
        # TODO: support partial parsing, do not disqualify the whole grammar
        # TODO: no caching for fitness score?

        while len(new_population) < self.population_size:
            parent1, _ = random.choice(selected)
            parent2, _ = random.choice(selected)
            child1, child2 = self.crossover(parent1, parent2, self.extra_arg)
            child1, fitness1 = self.mutate(child1, self.extra_arg)
            child2, fitness2 = self.mutate(child2, self.extra_arg)
            new_population.append((child1, fitness1))
            if len(new_population) < self.population_size:
                new_population.append((child2, fitness2))
        self.population = new_population

    def run(self):
        for generation in range(self.max_generations):
            best_individual = min(self.population, key=lambda individual: individual[1])
            self.fitness_history.append(best_individual[1])
            if self.best_individual is None or best_individual[1] < self.best_individual[1]:
                self.best_individual = best_individual

            self.logger.info(f"Generation {generation}, Best Fitness: {best_individual[1]}")
            if generation > 0 and self.fitness_history[-1] == self.fitness_history[-2]:
                self.best_fitness_stagnant_counter += 1
            else:
                self.best_fitness_stagnant_counter = 0

            if self.best_fitness_stagnant_counter >= self.early_stop_generations:
                self.logger.info(f"Early stopping triggered after {generation} generations due to stagnant fitness.")
                break

            self.evolve()
        return self.best_individual

    def plot_fitness_history(self):
        sns.set(style="darkgrid")
        plt.figure(figsize=(10, 6))
        plt.plot(self.fitness_history, label="Best Fitness")
        plt.title("Fitness History Over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness")
        plt.legend()
        plt.show()
