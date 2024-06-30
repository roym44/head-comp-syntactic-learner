from input.BlankGrammars import *
from learner.experiment import *
from learner.general_case_configs import *

# learner config
LEARNERS = ("Kayne", "Language", "Category", "Word")
THEORIES = ("Head-initial", "Head-final", "Mixed-category", "Mixed-word")
ALL_CONFIGS = {l: THEORIES for l in LEARNERS}

# general
LOGS_FOLDER = os.path.join("output", "logs")


def random_exp():
    pass


def general_case_compare_exp():
    """
    This experiment tests the "General Case" for the learners. That means there is no coordination.
    Pages 49 - 60 in Avraham's work, using the same input he generated.
    """
    exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO)
    # exp.test_learner("Kayne", "Head-initial", algorithms=["GA"], target=GRAMMAR_511, initial_input=INPUT_511)
    exp.test_learner("Kayne", "Head-final", algorithms=["GA"], target=GRAMMAR_512, initial_input=INPUT_512)
    # exp.test_learner("Kayne", "Mixed-category", algorithms=["SA", "GA"], target=GRAMMAR_513, initial_input=INPUT_513)
    # exp.test_learner("Kayne", "Mixed-word", algorithms=["SA", "GA"], target=GRAMMAR_514, initial_input=INPUT_514)


def coord_compare_exp():
    # with coordination (including "and")
    exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP)
    exp.test_learner("Kayne", "Head-initial", coordination=True, algorithms=["SA", "GA"])
    # exp.sanity_test(ALL_CONFIGS, coordination=True)


if __name__ == '__main__':
    general_case_compare_exp()
    # coord_exp()
