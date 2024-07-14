import os

from input.BlankGrammars import *
from learner.experiment.experiment import Experiment
from learner.experiment.general_case_config import *

LEARNERS = ("Kayne", "Language", "Category", "Word")
THEORIES = ("Head-initial", "Head-final", "Mixed-category", "Mixed-word")
ALL_CONFIGS = {l: THEORIES for l in LEARNERS}
LOGS_FOLDER = os.path.join("output", "logs")
PLOTS_FOLDER = os.path.join("output", "plots")


def general_case_exp():
    """
    This experiment tests the "General Case" for the learners. That means there is no coordination.
    Pages 49 - 60 in Avraham's work, using the same input he generated.
    """
    exp = Experiment(LOGS_FOLDER, PLOTS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO)
    # Kayne
    # exp.test_learner("Kayne", "Head-initial", algorithms=["GA"], initial_input=INPUT_511)
    exp.test_learner("Kayne", "Head-final", algorithms=["GA"], initial_input=INPUT_512)
    # exp.test_learner("Kayne", "Mixed-category", algorithms=["GA"], initial_input=INPUT_513)
    # exp.test_learner("Kayne", "Mixed-word", algorithms=["GA"], initial_input=INPUT_514)


def with_coordination_exp():
    # with coordination (including "and")
    exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP)
    exp.test_learner("Kayne", "Head-initial", coordination=True, algorithms=["SA", "GA"])
    # exp.sanity_test(ALL_CONFIGS, coordination=True)


if __name__ == '__main__':
    general_case_exp()
