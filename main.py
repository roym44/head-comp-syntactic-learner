from learner.sa.SimulatedAnnealingLearner import *

def previous_runs():
    run_learner()
    sanity_test(pp = True, cp = True, coordination = True)
    test_learner("Kayne", "Head-final", pp=True, cp=True, coordination=True, user_input=False, input_size=100)

if __name__ == '__main__':
    test_learner("Kayne", "Head-final", pp=True, cp=True, coordination=True, user_input=False, input_size=10)
