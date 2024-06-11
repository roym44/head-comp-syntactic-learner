from input.BlankGrammars import *
from learner.experiment import *


# learner config
LEARNERS = ("Kayne", "Language", "Category", "Word")
THEORIES = ("Head-initial", "Head-final", "Mixed-category", "Mixed-word")
ALL_CONFIGS = { l : THEORIES for l in LEARNERS}

# general
LOGS_FOLDER = os.path.join("output", "logs")

if __name__ == '__main__':
    # with coordination (including "and")
    # exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP, "SA")
    # exp.test_learner("Kayne", "Head-initial", pp=True, cp=True, coordination=True)

    # no coordination
    exp = Experiment(LOGS_FOLDER, KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO, "SA")
    exp.test_learner("Kayne", "Head-initial", pp=True, cp=True, coordination=False)

    # exp.test_learner("Kayne", "Head-final", pp=True, cp=True, coordination=False)
    # exp.sanity_test(ALL_CONFIGS, pp=True, cp=True, coordination=False)
