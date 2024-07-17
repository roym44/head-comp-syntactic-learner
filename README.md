# head-comp-syntactic-learner

## How to run the learner

To run the learning experiment, run `main.py`.
Currently, it runs a sanity test which means it runs every type of input on every type of learner (16 scenarios).
The experiment has several parameters:
- pp - whether to use PPs in the input. 
- cp - whether to use CPs in the input. 
- coordination - whether to have coordination structures in the input (the word "and"). 
- input_size - how many input items to generate (default - 50). 
- temperature - the initial temperature for the SA learner (default - 100).

It is also possible to run the function test_learner which only runs one scenario.
Its parameters are the type of learner, the type of input and then almost the same parameters as sanity_test.

## Resources
- The logs for each run of the learner are saved in the folder `logs`. 
- When running the parser, a parse tree can be generated. It will be saved to the folder `resources`.

## Other notes

- The blank grammar being used is `KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO` in the file `BlankGrammars.py`. 
- The possible neighbour functions are in the variable `self.neighbour_functions` in the file `MinimalistGrammarAnnealer.py`. 
  - This variable is initialized in the function `set_learner_type` and further modified in the function `random_neighbour` (so changes must be made in both places). 
- The learner uses a numbered version of the parser - `NumberBottomUpParser.py`.
  - The original parser is in `BottomUpParser.py` and might not work. 
  - The numbered parser translates the grammar items from their textual version to their numbered version and then parses.

### Credits
- Original codebase written by [Tomer Avraham](https://bitbucket.org/taucompling/headcomplementsyntacticlearner/).
- GA base class written by [Matan Abudy](https://github.com/matanabudy/simple-genetic-algorithm-varying-lengths).