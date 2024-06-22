from input.BlankGrammars import *
from learner.experiment import *


# learner config
LEARNERS = ("Kayne", "Language", "Category", "Word")
THEORIES = ("Head-initial", "Head-final", "Mixed-category", "Mixed-word")
ALL_CONFIGS = { l : THEORIES for l in LEARNERS}

# general
LOGS_FOLDER = os.path.join("output", "logs")

def basic_exp():
    # no coordination
    exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO)
    exp.test_learner("Kayne", "Head-initial", algorithms=["GA"], target_grammar=GRAMMAR_TARGET_HI)
    # exp.test_learner("Kayne", "Head-final", algorithms=["SA", "GA"])
    # exp.sanity_test(ALL_CONFIGS)

def coord_exp():
    # with coordination (including "and")
    exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP)
    exp.test_learner("Kayne", "Head-initial", coordination=True, algorithms=["SA", "GA"])
    # exp.sanity_test(ALL_CONFIGS, coordination=True)

if __name__ == '__main__':
    basic_exp()
    # coord_exp()