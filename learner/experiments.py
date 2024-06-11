import os
from loguru import logger

from learner.sa.SimulatedAnnealingLearner import *
from input.BlankGrammars import *

# experiment configuration
LOGS_FOLDER = os.path.join("output", "logs")
blank_grammar = KAYNE_GRAMMAR_WITH_EMPTY_DP


def init_log_file(learner, text_input, pp, cp):
    run_string = "%s, %s" % (learner, text_input)
    elements = []
    if pp:
        elements.append("PP")
    if cp:
        elements.append("CP")
    if elements:
        run_string += ", " + " & ".join(elements)
    log_file_name = time.strftime("log_%Y_%m_%d__%H_%M_%S") + " - %s.txt" % (run_string,)
    logger.add(os.path.join(LOGS_FOLDER, log_file_name))


def generate_input(input_type, pp, cp, coordination, size=50):
    with_pp = None
    with_cp = None
    if input_type == "Head-initial":
        if pp:
            with_pp = "initial"
        if cp:
            with_cp = "initial"
        text_input = get_custom_text(size=size,
                                     with_transitive="initial",
                                     with_dp=None,
                                     with_prepositions=with_pp,
                                     with_cp=with_cp,
                                     with_coordination=coordination,
                                     recursion_depth=1)
    elif input_type == "Head-final":
        if pp:
            with_pp = "final"
        if cp:
            with_cp = "final"
        text_input = get_custom_text(size=size,
                                     with_transitive="final",
                                     with_dp=None,
                                     with_prepositions=with_pp,
                                     with_cp=with_cp,
                                     with_coordination=coordination,
                                     recursion_depth=1)
    elif input_type == "Mixed-category":
        if pp:
            with_pp = "final"
        if cp:
            with_cp = "initial"
        text_input = get_custom_text(size=size,
                                     with_transitive="initial",
                                     with_dp=None,
                                     with_prepositions=with_pp,
                                     with_cp=with_cp,
                                     with_coordination=coordination,
                                     recursion_depth=1)
    elif input_type == "Mixed-word":
        if pp:
            with_pp = "final"
        if cp:
            with_cp = "initial"
        text_input = get_custom_text(size=size,
                                     with_transitive="mixed",
                                     with_dp=None,
                                     with_prepositions=with_pp,
                                     with_cp=with_cp,
                                     with_coordination=coordination,
                                     recursion_depth=1)
    else:
        raise Exception(f"Invalid input type - {input_type}")

    text_input = text_input[:-1].split("#")
    return text_input


def test_learner(learner_type, input_type, pp=True, cp=False, coordination=False,
                 input_size=50, user_input=False, temperature=100):
    init_log_file(learner_type, input_type, pp, cp)
    print("Time: %s" % (time.strftime("%Y_%m_%d__%H_%M_%S: "),))

    initial_input = generate_input(input_type, pp, cp, coordination, input_size)
    logger.info("Input is: %s" % (initial_input,))

    global blank_grammer

    annealer = MinimalistGrammarAnnealer(logger, initial_input, blank_grammar, learner_type)
    logger.info("Initial Temperature: %f" % (temperature,))
    learner = SimulatedAnnealingLearner(logger, annealer, temperature)

    if user_input:
        while True:
            initial_input = input("Steps: ")
            if initial_input == 'd':
                import pdb;
                pdb.set_trace()
            steps = int(initial_input)
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


def sanity_test(pp=True, cp=True, coordination=False, input_size=50, temperature=100, items_to_run=None):
    # Kayne learner:
    kayne_times = []
    kayne_results = []

    if items_to_run is None:
        items_to_run = list(range(1, 17))

    if 1 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Head-initial", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)

    if 2 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Head-final", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)

    if 3 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Mixed-category", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)

    if 4 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Kayne", "Mixed-word", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        kayne_results.append(final_hypothesis)
        kayne_times.append(time.time() - start_time)

    # Language learner:
    language_times = []
    language_results = []

    if 5 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Head-initial", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)

    if 6 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Head-final", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)

    if 7 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Mixed-category", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)

    if 8 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Language", "Mixed-word", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        language_results.append(final_hypothesis)
        language_times.append(time.time() - start_time)

    # Category learner:
    category_times = []
    category_results = []

    if 9 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Head-initial", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)

    if 10 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Head-final", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)

    if 11 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Mixed-category", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)

    if 12 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Category", "Mixed-word", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        category_results.append(final_hypothesis)
        category_times.append(time.time() - start_time)

    # Word learner:
    word_times = []
    word_results = []

    if 13 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Head-initial", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)

    if 14 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Head-final", pp=pp, cp=cp, coordination=coordination, user_input=False,
                                        input_size=input_size, temperature=temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)

    if 15 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Mixed-category", pp=pp, cp=cp, coordination=coordination,
                                        user_input=False, input_size=input_size, temperature=temperature)
        word_results.append(final_hypothesis)
        word_times.append(time.time() - start_time)

    if 16 in items_to_run:
        start_time = time.time()
        final_hypothesis = test_learner("Word", "Mixed-word", pp=pp, cp=cp, coordination=coordination, user_input=False,
                                        input_size=input_size, temperature=temperature)
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
