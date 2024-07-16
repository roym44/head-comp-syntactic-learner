import os

from input.BlankGrammars import *
from learner.experiment.experiment import Experiment
from learner.experiment.general_case_config import *

LEARNERS = ("Kayne", "Language", "Category", "Word")
THEORIES = ("Head-initial", "Head-final", "Mixed-category", "Mixed-word")
ALGORITHMS = ["SA", "GA"]
ALL_CONFIGS = {l: THEORIES for l in LEARNERS}
LOGS_FOLDER = os.path.join("output", "logs")
PLOTS_FOLDER = os.path.join("output", "plots")

# for a coordination experiment - use KAYNE_GRAMMAR_WITH_EMPTY_DP
def general_case_exp():
    """
    This experiment tests the "General Case" for the learners. That means there is no coordination.
    Pages 49 - 60 in Avraham's work, using the same input he generated.
    """
    exp = Experiment(LOGS_FOLDER, PLOTS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO)

    # Kayne - 5.1
    exp.test_learner("Kayne", "Head-initial", algorithms=ALGORITHMS, initial_input=INPUT_511)
    # exp.test_learner("Kayne", "Head-final", algorithms=ALGORITHMS, initial_input=INPUT_512)
    # exp.test_learner("Kayne", "Mixed-category", algorithms=ALGORITHMS, initial_input=INPUT_513)
    # exp.test_learner("Kayne", "Mixed-word", algorithms=ALGORITHMS, initial_input=INPUT_514)

    # Language - 5.2
    # exp.test_learner("Language", "Head-initial", algorithms=ALGORITHMS, initial_input=INPUT_521)
    # exp.test_learner("Language", "Head-final", algorithms=ALGORITHMS, initial_input=INPUT_522)
    # exp.test_learner("Language", "Mixed-category", algorithms=ALGORITHMS, initial_input=INPUT_523)
    # exp.test_learner("Language", "Mixed-word", algorithms=ALGORITHMS, initial_input=INPUT_524)

    # Category - 5.3
    # exp.test_learner("Category", "Head-initial", algorithms=ALGORITHMS, initial_input=INPUT_531)
    # exp.test_learner("Category", "Head-final", algorithms=ALGORITHMS, initial_input=INPUT_532)
    # exp.test_learner("Category", "Mixed-category", algorithms=ALGORITHMS, initial_input=INPUT_533)
    # exp.test_learner("Category", "Mixed-word", algorithms=ALGORITHMS, initial_input=INPUT_534)

    # Word - 5.4
    # exp.test_learner("Word", "Head-initial", algorithms=ALGORITHMS, input_size=INPUT_541)
    # exp.test_learner("Word", "Head-final", algorithms=ALGORITHMS, initial_input=INPUT_542)
    # exp.test_learner("Word", "Mixed-category", algorithms=ALGORITHMS, initial_input=INPUT_543)
    # exp.test_learner("Word", "Mixed-word", algorithms=ALGORITHMS, initial_input=INPUT_544)


if __name__ == '__main__':
    general_case_exp()
