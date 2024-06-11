from input.BlankGrammars import *
from learner.experiment import *


# learner config
LEARNERS = ("Kayne", "Language", "Category", "Word")
THEORIES = ("Head-initial", "Head-final", "Mixed-category", "Mixed-word")
LEARNER_CONFIGS = { l : THEORIES for l in LEARNERS}

BLANK_GRAMMAR = KAYNE_GRAMMAR_WITH_EMPTY_DP

# general
LOGS_FOLDER = os.path.join("output", "logs")

if __name__ == '__main__':
    exp = Experiment(LOGS_FOLDER, BLANK_GRAMMAR, "SA")
    exp.sanity_test(LEARNER_CONFIGS, pp=True, cp=True, coordination=False)
