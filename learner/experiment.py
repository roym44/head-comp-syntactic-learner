import os
from loguru import logger

from learner.sa.SimulatedAnnealingLearner import *


class Experiment(object):
    def __init__(self, logs_folder, blank_grammar, algorithm):
        self.logs_folder = logs_folder
        self.blank_grammar = blank_grammar
        self.algorithm = algorithm
        # logger.remove() # remove stdout logger
        self.current_sink = None

    def init_log_file(self, learner, text_input, pp, cp):
        run_string = f"{learner}, {text_input}"
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
        annealer = MinimalistGrammarAnnealer(logger, initial_input, self.blank_grammar, learner_type)
        logger.info("Initial Temperature: %f" % (temperature,))
        learner = SimulatedAnnealingLearner(logger, annealer, temperature)
        previous_hypothesis = learner.hypothesis
        while learner.iteration % 300 == 0:
            learner.anneal(300)
            if previous_hypothesis == learner.hypothesis:
                break
            previous_hypothesis = learner.hypothesis
        return learner.hypothesis

    def learn_ga(self, initial_input, learner_type):
        raise Exception("Genetic Algorithm not implemented")

    def test_learner(self, learner_type, input_type, pp=True, cp=False, coordination=False,
                     input_size=50, temperature=100):
        """
        Testing a specific learner with a specific input
        """
        self.init_log_file(learner_type, input_type, pp, cp)
        logger.info(f"Time: {time.strftime('%Y_%m_%d__%H_%M_%S: ')}")

        initial_input = self.generate_input(input_type, pp, cp, coordination, input_size)
        logger.info("Input is: %s" % (initial_input,))

        if self.algorithm == "SA":
            hypothesis = self.learn_sa(initial_input, learner_type, temperature)
        elif self.algorithm == "GA":
            hypothesis = self.learn_ga(initial_input, learner_type)
        else:
            raise Exception("Unsupported algorithm")
        return hypothesis

    def sanity_test(self, learner_configs, pp=True, cp=True, coordination=False, input_size=50, temperature=100):
        """
        Testing all learners with their configurations according to the learner_configs dictionary
        """
        for learner, configs in learner_configs.items():
            print(f"{learner} learner:")
            for config in configs:
                start_time = time.time()
                final_hypothesis = self.test_learner(learner, config, pp=pp, cp=cp, coordination=coordination,
                                                     input_size=input_size, temperature=temperature)
                elapsed_time = time.time() - start_time
                print(f"{config}: {elapsed_time:.2f}s - {final_hypothesis}")
