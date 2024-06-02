
import os
import sys
import math
import time
import random

from MinimalistGrammarAnnealer import MinimalistGrammarAnnealer
from InputGenerator import *
from BlankGrammars import *

LOGS_FOLDER = "logs"

log_file = None

def log(line):
    time_str = time.strftime("%Y_%m_%d__%H_%M_%S: ")
    log_file.write(time_str + line + "\n")
    print(line)
    log_file.flush()

class SimulatedAnnealingLearner(object):
    
    def __init__(self, annealer, input, initial_temperature, initial_hypothesis = None):
        self.annealer = annealer
        
        if initial_hypothesis:
            self.hypothesis = initial_hypothesis
        else:
            self.hypothesis = self.annealer.get_initial_hypothesis()
        log("Initial hypothesis: %s" % (self.hypothesis, ))
        self.temperature = initial_temperature
        self.iteration = 0
        self.total_time = 0
        
    def anneal(self, steps):
        start = time.time()
        total_steps = self.iteration + steps
        self.current_energy = self.annealer.energy(self.hypothesis)
        self.annealer.input_parsing_dict = self.annealer.new_parsing_dict
        for i in range(steps):
            log("\nIteration: %d" % (self.iteration, ))
            print("Time: %s" % (time.strftime("%Y_%m_%d__%H_%M_%S: "), ))
            log("Hypothesis: %s" % (self.hypothesis, ))
            log("Energy: %d" % (self.current_energy, ))
            log("Temperature: %f" % (self.temperature, ))
            # I made the neighbour function also calculate the energy to save time.
            new_hypothesis, new_energy = self.annealer.random_neighbour(self.hypothesis)
            if new_hypothesis is not None:
                log("New Energy: %d" % (new_energy, ))
                delta = new_energy - self.current_energy
                log("Delta: %d" % (delta, ))
                if delta <= 0:
                    p = 1
                else:
                    p = math.e ** (0 - (delta / self.temperature))
                log("Change probability: %f" % (p, ))
                if random.random() < p and self.hypothesis != new_hypothesis:
                    self.hypothesis = new_hypothesis
                    self.current_energy = new_energy
                    self.annealer.input_parsing_dict = self.annealer.new_parsing_dict
                    log("Changed hypotheses.")
                else:
                    log("Didn't change hypotheses.")
            else:
                log("Didn't change hypotheses.")

            self.temperature = 0.997 * self.temperature
            self.iteration += 1
            
            if self.temperature < 0.5:
                break
            
        elapsed = time.time() - start
        self.total_time += elapsed
            
        log("\nIteration: %d\nHypothesis: %s\nEnergy: %d\nTemperature: %f\nElapsed time: %d\n" % (self.iteration, self.hypothesis, self.current_energy, self.temperature, time.time() - start))
        return self.iteration, self.hypothesis, self.temperature
        
def test_annealing(input):
    input = input[:-1].split("#")    
    log("Input is: %s" % (input, ))
    
    annealer = MinimalistGrammarAnnealer(input)
    hyp = annealer.get_initial_hypothesis()
    log("Initial hypothesis: %s" % (hyp, ))
    initial_energy = annealer.energy(hyp)
    log("Initial Energy: %d" % (initial_energy, ))
    
    temperature = int(input("Temperature: "))
    
    learner = SimulatedAnnealingLearner(annealer, input, temperature)
    while True:
        steps = int(input("Steps: "))
        learner.anneal(steps)
        
def init_log_file(learner, input, pp, cp):
    run_string = "%s, %s" % (learner, input)
    elements = []
    if pp:
        elements.append("PP")
    if cp:
        elements.append("CP")
    if elements:
        run_string += ", " + " & ".join(elements)
    log_file_name = time.strftime("log_%Y_%m_%d__%H_%M_%S") + " - %s.txt" % (run_string, )
    log_path = os.path.join(LOGS_FOLDER, log_file_name)
    global log_file
    log_file = open(log_path, 'w')
    return log_file
    
def generate_input(input_type, pp, cp, coordination, size = 50):
    with_pp = None
    with_cp = None
    if input_type == "Head-initial":
        if pp:
            with_pp = "initial"
        if cp:
            with_cp = "initial"
        input = get_custom_text(size = size,
                                with_transitive = "initial",
                                with_dp = None,
                                with_prepositions = with_pp,
                                with_cp = with_cp,
                                with_coordination = coordination,
                                recursion_depth = 1)
    elif input_type == "Head-final":
        if pp:
            with_pp = "final"
        if cp:
            with_cp = "final"
        input = get_custom_text(size = size,
                                with_transitive = "final",
                                with_dp = None,
                                with_prepositions = with_pp,
                                with_cp = with_cp,
                                with_coordination = coordination,
                                recursion_depth = 1)
    elif input_type == "Mixed-category":
        if pp:
            with_pp = "final"
        if cp:
            with_cp = "initial"
        input = get_custom_text(size = size,
                                with_transitive = "initial",
                                with_dp = None,
                                with_prepositions = with_pp,
                                with_cp = with_cp,
                                with_coordination = coordination,
                                recursion_depth = 1)
    elif input_type == "Mixed-word":
        if pp:
            with_pp = "final"
        if cp:
            with_cp = "initial"
        input = get_custom_text(size = size,
                                with_transitive = "mixed",
                                with_dp = None,
                                with_prepositions = with_pp,
                                with_cp = with_cp,
                                with_coordination = coordination,
                                recursion_depth = 1)
    else:
        raise Exception("Invalid input type - %" % (input_type, ))
        
    input = input[:-1].split("#")
    return input

def test_learner(learner_type, input_type, pp = True, cp = False, coordination = False, input_size = 50, user_input = False, temperature = 100):
    log_file = init_log_file(learner_type, input_type, pp, cp)
    print("Time: %s" % (time.strftime("%Y_%m_%d__%H_%M_%S: "), ))
    
    input = generate_input(input_type, pp, cp, coordination, input_size)
    log("Input is: %s" % (input, ))
    
    global blank_grammer
    
    annealer = MinimalistGrammarAnnealer(input, blank_grammar, learner_type, log)
    
    log("Initial Temperature: %f" % (temperature, ))
    
    learner = SimulatedAnnealingLearner(annealer, input, temperature)
    
    if user_input:
        while True:
            input = input("Steps: ")
            if input == 'd':
                import pdb; pdb.set_trace()
            steps = int(input)
            learner.anneal(steps)
    else:
        previous_hypothesis = learner.hypothesis
        while learner.iteration % 300 == 0:
            learner.anneal(300)
            if previous_hypothesis == learner.hypothesis:
                break
            else:
                previous_hypothesis = learner.hypothesis
        
    return learner.hypothesis
    
def sanity_test(pp = True, cp = True, coordination = False, input_size = 50, temperature = 100, items_to_run = None):
    # Kayne learner:
    kayne_times = []
    kayne_results = []
    
    if items_to_run is None:
        items_to_run = list(range(1, 17))
    
    if 1 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Head-initial", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)
    
    if 2 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Head-final", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)
    
    if 3 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Mixed-category", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)
        
    if 4 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Mixed-word", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)
    
    # Language learner:
    language_times = []
    language_results = []
    
    if 5 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Head-initial", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)
    
    if 6 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Head-final", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)
    
    if 7 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Mixed-category", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)
    
    if 8 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Mixed-word", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)
    
    # Category learner:
    category_times = []
    category_results = []
    
    if 9 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Head-initial", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)
    
    if 10 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Head-final", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)
    
    if 11 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Mixed-category", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)
    
    if 12 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Mixed-word", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)
    
    # Word learner:
    word_times = []
    word_results = []
    
    if 13 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Head-initial", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)
    
    if 14 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Head-final", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)
    
    if 15 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Mixed-category", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)
    
    if 16 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Mixed-word", pp = pp, cp = cp, coordination = coordination, user_input = False, input_size = input_size, temperature = temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)
    
    # Print results:
    print("Kayne learner:")
    if 1 in items_to_run: print("Head-initial: %ss - %s" % (kayne_times[0], kayne_results[0]))
    if 2 in items_to_run: print("Head-final: %ss - %s" % (kayne_times[1], kayne_results[1]))
    if 3 in items_to_run: print("Mixed-category: %ss - %s" % (kayne_times[2], kayne_results[2]))
    if 4 in items_to_run: print("Mixed-word: %ss - %s" % (kayne_times[3], kayne_results[3]))
    
    print("Language learner:")
    if 5 in items_to_run: print("Head-initial: %ss - %s" % (language_times[0], language_results[0]))
    if 6 in items_to_run: print("Head-final: %ss - %s" % (language_times[1], language_results[1]))
    if 7 in items_to_run: print("Mixed-category: %ss - %s" % (language_times[2], language_results[2]))
    if 8 in items_to_run: print("Mixed-word: %ss - %s" % (language_times[3], language_results[3]))
    
    print("Category learner:")
    if 9 in items_to_run: print("Head-initial: %ss - %s" % (category_times[0], category_results[0]))
    if 10 in items_to_run: print("Head-final: %ss - %s" % (category_times[1], category_results[1]))
    if 11 in items_to_run: print("Mixed-category: %ss - %s" % (category_times[2], category_results[2]))
    if 12 in items_to_run: print("Mixed-word: %ss - %s" % (category_times[3], category_results[3]))
    
    print("Word learner:")
    if 13 in items_to_run: print("Head-initial: %ss - %s" % (word_times[0], word_results[0]))
    if 14 in items_to_run: print("Head-final: %ss - %s" % (word_times[1], word_results[1]))
    if 15 in items_to_run: print("Mixed-category: %ss - %s" % (word_times[2], word_results[2]))
    if 16 in items_to_run: print("Mixed-word: %ss - %s" % (word_times[3], word_results[3]))
    
def run_learner():
    log_file_name = time.strftime("log_%Y_%m_%d__%H_%M_%S.txt")
    log_path = os.path.join(LOGS_FOLDER, log_file_name)
    global log_file
    log_file = open(log_path, 'w')
    print("Time: %s" % (time.strftime("%Y_%m_%d__%H_%M_%S: "), ))
    
    # Head initial:
    input = get_custom_text(size = 50, with_transitive = "initial", with_dp = None, with_prepositions = "initial", with_cp = None, recursion_depth = 1)
    
    # Head final:
    # input = get_custom_text(size = 50, with_transitive = "final", with_dp = None, with_prepositions = "final", with_cp = "final", recursion_depth = 1)
    
    # Variation by category:
    # input = get_custom_text(size = 50, with_transitive = "initial", with_dp = None, with_prepositions = "final", with_cp = "initial", recursion_depth = 1)
    
    # Variation by word:
    # input = get_custom_text(size = 50, with_transitive = "mixed", with_dp = None, with_prepositions = "mixed", with_cp = "mixed", recursion_depth = 1)
    
    blank_grammar = KAYNE_GRAMMAR
    
    input = input[:-1].split("#")    
    log("Input is: %s" % (input, ))
    
    annealer = MinimalistGrammarAnnealer(input, blank_grammar, "Kayne", log)
    
    temperature = 1000
    log("Initial Temperature: %f" % (temperature, ))
    
    learner = SimulatedAnnealingLearner(annealer, input, temperature)
    while True:
        input = input("Steps: ")
        if input == 'd':
            import pdb; pdb.set_trace()
        steps = int(input)
        learner.anneal(steps)

if __name__ == '__main__':
    blank_grammar = KAYNE_GRAMMAR_WITH_EMPTY_DP # Works with impossible category, not always for naive deletion. Works slow.
    
    # run_learner()
    sanity_test(pp = True, cp = True, coordination = True)
    # test_learner("Kayne", "Head-final", pp = True, cp = True, coordination = True, user_input = False, input_size = 100)
    
    
    