import os
from loguru import logger

from learner.sa.SimulatedAnnealingLearner import *
from learner.ga.ga import *
from learner.ga.mg_ga import *
from parser.NumberBottomUpParser import parse_sentence
from minimalist_grammar import NumberMinimalistGrammarTree


class Experiment(object):
    def __init__(self, logs_folder, blank_grammar):
        self.logs_folder = logs_folder
        self.blank_grammar = blank_grammar
        # logger.remove() # remove stdout logger
        self.current_sink = None

    def init_log_file(self, learner, text_input, pp, cp, algorithm):
        run_string = f"{learner}, {algorithm}, {text_input}"
        elements = []
        if pp:
            elements.append("PP")
        if cp:
            elements.append("CP")
        if elements:
            run_string += ", " + " & ".join(elements)
        log_file_name = f"log_{time.strftime('%Y_%m_%d__%H_%M_%S')} - {run_string}.txt"
        # we stop writing to current log file and start writing to the new one
        if self.current_sink is not None:
            logger.remove(self.current_sink)
        self.current_sink = logger.add(os.path.join(self.logs_folder, log_file_name))
        return log_file_name

    def generate_input(self, input_type, pp, cp, coordination, size=50):
        transitive_types = {
            "Head-initial": "initial",
            "Head-final": "final",
            "Mixed-category": "initial",
            "Mixed-word": "mixed"
        }
        prepositions = {
            "Head-initial": "initial",
            "Head-final": "final",
            "Mixed-category": "final",
            "Mixed-word": "final"
        }
        complementizers = {
            "Head-initial": "initial",
            "Head-final": "final",
            "Mixed-category": "initial",
            "Mixed-word": "initial"
        }

        if input_type not in transitive_types:
            raise Exception(f"Invalid input type - {input_type}")

        with_pp = prepositions[input_type] if pp else None
        with_cp = complementizers[input_type] if cp else None

        text_input = get_custom_text(size=size,
                                     with_transitive=transitive_types[input_type],
                                     with_dp=None,
                                     with_prepositions=with_pp,
                                     with_cp=with_cp,
                                     with_coordination=coordination,
                                     recursion_depth=1)

        text_input = text_input[:-1].split("#")
        return text_input

    def learn_sa(self, initial_input, learner_type, temperature):
        mga = MinimalistGrammarAnnealer(logger, initial_input, self.blank_grammar, learner_type)
        logger.info("Initial Temperature: %f" % (temperature,))
        sal = SimulatedAnnealingLearner(logger, mga, temperature)
        previous_hypothesis = sal.hypothesis
        while sal.iteration % 300 == 0:
            sal.anneal(300)
            if previous_hypothesis == sal.hypothesis:
                break
            previous_hypothesis = sal.hypothesis
        return sal.hypothesis, sal.current_energy

    def learn_ga(self, initial_input, learner_type):
        mga = MinimalistGrammarAnnealer(logger, initial_input, self.blank_grammar, learner_type)
        mg_ga = MGGA(mga)
        gal = GeneticAlgorithm(
            logger,
            mg_ga.evaluate_fitness_grammar,
            mg_ga.mutate_grammar,
            mg_ga.crossover_grammar,
            generate_individual=mg_ga.generate_individual_grammar,
            population_size=5,
            max_generations=1000,
            early_stop_generations=50,
            tournament_size=2,
        )
        best_individual, best_fitness = gal.run()
        logger.info(f"Best individual: {best_individual}, fitness: {best_fitness}")
        gal.plot_fitness_history()
        return best_individual, best_fitness

    def get_target_hypothesis(self, initial_input, grammar, learner_type):
        # abuses the current implementation of the MinimalistGrammarAnnealer (get_target_hypothesis)
        mga = MinimalistGrammarAnnealer(logger, initial_input, grammar, learner_type)
        target_hyp = mga.get_initial_hypothesis()
        target_score = mga.energy(target_hyp)
        return target_hyp, target_score

    def test_learner(self, learner_type, input_type, pp=True, cp=True, coordination=False,
                     input_size=50, temperature=100, algorithms=None, target=None, initial_input=None, print_samples=True):
        """
        Testing a specific learner with a specific input
        Retrieves the target hypothesis and prints it in the end in order to compare.
        """
        if initial_input is None:
            initial_input = self.generate_input(input_type, pp, cp, coordination, input_size)

        if print_samples:
            # we need this apparently to draw the tree
            NumberMinimalistGrammarTree.WITH_NESTED_DERIVATION = True

        target_hyp, target_score = self.get_target_hypothesis(initial_input, target, learner_type)
        for a in algorithms:
            log_file_name = self.init_log_file(learner_type, input_type, pp, cp, a)
            logger.info(f"Input is: {initial_input}")
            logger.info(f"Time: {time.strftime('%Y_%m_%d__%H_%M_%S: ')}")
            logger.info(f"pp: {pp}, cp: {cp}, coordination: {coordination}, input_size: {input_size}")

            start_time = time.time()
            if a == "SA":
                hypothesis, score = self.learn_sa(initial_input, learner_type, temperature)
            elif a == "GA":
                hypothesis, score = self.learn_ga(initial_input, learner_type)
            else:
                raise Exception("Unsupported algorithm")
            elapsed_time = time.time() - start_time
            logger.info(f"Input was: {initial_input}")
            logger.info(f"Final hypothesis: {hypothesis.get_sorted_lexicon()}, score: {score}")
            logger.info(f"Target hypothesis: {target_hyp.get_sorted_lexicon()}, score: {target_score}, "
                        f"difference: {score - target_score}")
            logger.info(f"Elapsed time: {elapsed_time:.2f}s")

            # print the tree derivation of some sentences from the input
            if print_samples:
                sentences = initial_input[:5]
                for sentence in sentences:
                    parse_sentence(hypothesis, sentence, draw_tree=True, folder=log_file_name)

    def sanity_test(self, learner_configs, pp=True, cp=True, coordination=False,
                    input_size=50, temperature=100, algorithms=None):
        """
        Testing all learners with their configurations according to the learner_configs dictionary
        """
        for learner, configs in learner_configs.items():
            print(f"{learner} learner:")
            for config in configs:
                start_time = time.time()
                self.test_learner(learner, config, pp=pp, cp=cp, coordination=coordination,
                                                     input_size=input_size, temperature=temperature,
                                                     algorithms=algorithms)
                elapsed_time = time.time() - start_time
                print(f"{config}: {elapsed_time:.2f}s")
