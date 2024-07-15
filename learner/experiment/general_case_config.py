import ast

from minimalist_grammar.MinimalistGrammar import MinimalistGrammar
from minimalist_grammar.MinimalistGrammarTree import MinimalistGrammarTree

# Expected Grammars
# TODO: this is only a partial list
LEXICON_G1 = [MinimalistGrammarTree(tree) for tree in [
    "[>@: DP =DP -O]s", "[>@: IP =VP =DP]s", "[>@: VP =PP =VP]s", "[>@: IP =IP -Comp]s",
    "[>Jerry: DP]s", "[>George: DP]s", "[>Elaine: DP]s", "[>Kramer: DP]s",
    "[>ran: VP]s", "[>walked: VP]s", "[>read: VP]s", "[>wrote: VP]s",
    "[>liked: VP =DP]s", "[>saw: VP =DP]s", "[>loved: VP =DP]s", "[>hated: VP =DP]s",
    "[>with: PP =DP]s", "[>by: PP =DP]s", "[>above: PP =DP]s", "[>under: PP =DP]s", "[>that: CP =IP]s",
    "[>knows: VP =CP]s", "[>says: VP =CP]s", "[>thinks: VP =CP]s", "[>assumes: VP =CP]s"]]
GRAMMAR_G1 = MinimalistGrammar(LEXICON_G1)
LEXICON_G2 = [MinimalistGrammarTree(tree) for tree in [
    "[>@: DP =DP -O]s", "[>@: IP =VP =DP]s", "[>@: VP =PP =VP]s", "[>@: IP =IP -Comp]s",
    "[>Jerry: DP]s", "[>George: DP]s", "[>Elaine: DP]s", "[>Kramer: DP]s",
    "[>ran: VP]s", "[>walked: VP]s", "[>read: VP]s", "[>wrote: VP]s",
    "[>liked: VP =DP +O]s", "[>saw: VP =DP +O]s", "[>loved: VP =DP +O]s", "[>hated: VP =DP +O]s",
    "[>with: PP =DP +O]s", "[>by: PP =DP +O]s", "[>above: PP =DP +O]s", "[>under: PP =DP +O]s",
    "[>that: CP =IP +Comp -Oc]s",
    "[>knows: VP =CP +Oc]s", "[>says: VP =CP +Oc]s", "[>thinks: VP =CP +Oc]s", "[>assumes: VP =CP +Oc]s"]]
GRAMMAR_G2 = MinimalistGrammar(LEXICON_G2)

LEXICON_G3 = [MinimalistGrammarTree(tree) for tree in [
    "[>@: DP =DP -O]s", "[>@: IP =VP =DP]s", "[>@: VP =PP =VP]s", "[>@: IP =IP -Comp]s",
    "[<Jerry: DP]s", "[<George: DP]s", "[<Elaine: DP]s", "[<Kramer: DP]s",
    "[<ran: VP]s", "[<walked: VP]s", "[<read: VP]s", "[<wrote: VP]s",
    "[<liked: VP =DP]s", "[<saw: VP =DP]s", "[<loved: VP =DP]s", "[<hated: VP =DP]s",
    "[<with: PP =DP]s", "[<by: PP =DP]s", "[<above: PP =DP]s", "[<under: PP =DP]s", "[<that: CP =IP]s",
    "[<knows: VP =CP]s", "[<says: VP =CP]s", "[<thinks: VP =CP]s", "[<assumes: VP =CP]s"]]
GRAMMAR_G3 = MinimalistGrammar(LEXICON_G3)

def get_input_from_log(log_path):
    with open(log_path, "r") as f:
        lexicon = f.readline().split(": ")
        return ast.literal_eval(lexicon[2])

# Kayne learner - HI, HF, MC, MW
INPUT_511 = get_input_from_log("output/logs/General Case/01 - log_2017_05_10__02_40_42 - Kayne, Head-initial, PP & CP.txt")
INPUT_512 = get_input_from_log("output/logs/General Case/02 - log_2017_05_10__02_57_53 - Kayne, Head-final, PP & CP.txt")
INPUT_513 = get_input_from_log("output/logs/General Case/03 - log_2017_05_10__03_54_20 - Kayne, Mixed-category, PP & CP.txt")
INPUT_514 = get_input_from_log("output/logs/General Case/04 - log_2017_05_10__06_09_15 - Kayne, Mixed-word, PP & CP.txt")

# Language learner - HI, HF, MC, MW
INPUT_521 = get_input_from_log("output/logs/General Case/05 - log_2017_05_10__06_51_45 - Language, Head-initial, PP & CP.txt")
INPUT_522 = get_input_from_log("output/logs/General Case/06 - log_2017_05_10__13_38_44 - Language, Head-final, PP & CP.txt")
INPUT_523 = get_input_from_log("output/logs/General Case/07 - log_2017_05_10__14_45_15 - Language, Mixed-category, PP & CP.txt")
INPUT_524 = get_input_from_log("output/logs/General Case/08 - log_2017_05_10__20_19_58 - Language, Mixed-word, PP & CP.txt")

# Category learner - HI, HF, MC, MW
INPUT_531 = get_input_from_log("output/logs/General Case/09 - log_2017_05_10__21_17_43 - Category, Head-initial, PP & CP.txt")
INPUT_532 = get_input_from_log("output/logs/General Case/10 - log_2017_05_10__21_43_43 - Category, Head-final, PP & CP.txt")
INPUT_533 = get_input_from_log("output/logs/General Case/11 - log_2017_05_11__10_30_47 - Category, Mixed-category, PP & CP.txt")
INPUT_534 = get_input_from_log("output/logs/General Case/12 - log_2017_05_12__10_47_11 - Category, Mixed-word, PP & CP.txt")

# Word learner - HI, HF, MC, MW
INPUT_541 = get_input_from_log("output/logs/General Case/13 - log_2017_05_13__18_57_05 - Word, Head-initial, PP & CP.txt")
INPUT_542 = get_input_from_log("output/logs/General Case/14 - log_2017_05_12__18_11_05 - Word, Head-final, PP & CP.txt")
INPUT_543 = get_input_from_log("output/logs/General Case/15 - log_2017_05_10__19_25_25 - Word, Mixed-category, PP & CP.txt")
INPUT_544 = get_input_from_log("output/logs/General Case/16 - log_2017_05_13__02_56_34 - Word, Mixed-word, PP & CP.txt")
