How to run the learner:

Most files can be run individually to test their own functionality.

To run the learner itself, the file to run is SimulatedAnnealingLearner.py.
The scenario being run is at the very end of the file.
Currently it runs a sanity test which means it runs every type of input on every type of learner (16 scenarions).
The function sanity_test has several parameters:
* pp - whether to use PPs in the input.
* cp - whether to use CPs in the input.
* coordination - whether to have coordination structures in the input (the word "and").
* input_size - how many input items to generate (default - 50).
* temperature - the initial temperature for the learner (default - 100).
* items_to_run - a list of numbers between 1 and 16 of which scenarios to run (default - all of them).

It is also possible to run the function test_learner which only runs one scenario.
Its parameters are the type of learner, the type of input and then almost the same parameters as sanity_test.

The blank grammar being used is KAYNE_GRAMMAR_WITH_EMPTY_DP in the file BlankGrammars.py (as seen in line 381 in SimulatedAnnealingLearner.py).

The possible neighbour functions are in the variable self.neighbour_functions in the file MinimalistGrammarAnnealer.py.
This variable is initialized in the function set_learner_type and further modified in the function random_neighbour (so changes must be made in both places).

The learner used to use BottomUpParser.py as the parser. Since it was too slow, a numbered version was written - NumberBottomUpParser.py.
The numbered version has since been updated and improved - these changes aren't in the original parser so it might not work!!!
The numbered parser traslates the grammar items from their textual version to their numbered version and then parses.

The logs for each run of the learner are saved in the folder Learner Logs.

When running the parser, a parse tree can be generated. It will be saved to the folder Derivation Trees.

For any other questions, I'm available at tomerav@gmail.com.