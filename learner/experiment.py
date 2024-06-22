import os
from loguru import logger

from learner.sa.SimulatedAnnealingLearner import *
from learner.ga.ga import *
from learner.ga.mg_ga import *
from minimalist_grammar.MinimalistGrammarTree import MinimalistGrammarTree

LEXICON_TARGET_HI = [MinimalistGrammarTree(tree) for tree in [
    "[>@: DP =DP -O]s", "[>@: IP =VP =DP]s", "[>@: VP =PP =VP]s", "[>@: IP =IP -Comp]s",
    "[>Jerry: DP]s", "[>George: DP]s", "[>Elaine: DP]s", "[>Kramer: DP]s",
    "[>ran: VP]s", "[>walked: VP]s", "[>read: VP]s", "[>wrote: VP]s",
    "[>liked: VP =DP]s", "[>saw: VP =DP]s", "[>loved: VP =DP]s", "[>hated: VP =DP]s",
    "[>with: PP =DP]s", "[>by: PP =DP]s", "[>above: PP =DP]s", "[>under: PP =DP]s",
    "[>that: CP =IP]s",
    "[>knows: VP =CP]s", "[>says: VP =CP]s", "[>thinks: VP =CP]s", "[>assumes: VP =CP]s"]]
GRAMMAR_TARGET_HI = MinimalistGrammar(LEXICON_TARGET_HI)


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
        mga = MinimalistGrammarAnnealer(logger, initial_input, grammar, learner_type)
        target_hyp = mga.get_initial_hypothesis()
        target_score = mga.energy(target_hyp)
        return target_hyp, target_score

    def test_learner(self, learner_type, input_type, pp=True, cp=True, coordination=False,
                     input_size=50, temperature=100, algorithms=None, target_grammar=None):
        """
        Testing a specific learner with a specific input
        """
        initial_input = self.generate_input(input_type, pp, cp, coordination, input_size)
        target_hyp, target_score = self.get_target_hypothesis(initial_input, target_grammar, learner_type)
        for a in algorithms:
            self.init_log_file(learner_type, input_type, pp, cp, a)
            logger.info(f"Input is: {initial_input}")
            logger.info(f"Time: {time.strftime('%Y_%m_%d__%H_%M_%S: ')}")
            logger.info(f"pp: {pp}, cp: {cp}, coordination: {coordination}, input_size: {input_size}")
            if a == "SA":
                hypothesis, score = self.learn_sa(initial_input, learner_type, temperature)
            elif a == "GA":
                hypothesis, score = self.learn_ga(initial_input, learner_type)
            else:
                raise Exception("Unsupported algorithm")
            logger.info(f"Input was: {initial_input}")
            logger.info(f"Final hypothesis: {hypothesis.get_sorted_lexicon()}, score: {score}")
            logger.info(f"Target hypothesis: {target_hyp.get_sorted_lexicon()}, score: {target_score}, difference: {score - target_score}")

    def sanity_test(self, learner_configs, pp=True, cp=True, coordination=False,
                    input_size=50, temperature=100, algorithms=None):
        """
        Testing all learners with their configurations according to the learner_configs dictionary
        """
        for learner, configs in learner_configs.items():
            print(f"{learner} learner:")
            for config in configs:
                start_time = time.time()
                final_hypothesis = self.test_learner(learner, config, pp=pp, cp=cp, coordination=coordination,
                                                     input_size=input_size, temperature=temperature,
                                                     algorithms=algorithms)
                elapsed_time = time.time() - start_time
                print(f"{config}: {elapsed_time:.2f}s - {final_hypothesis}")
