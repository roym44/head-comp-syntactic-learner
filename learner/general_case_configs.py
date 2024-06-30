import ast

from minimalist_grammar.MinimalistGrammar import MinimalistGrammar
from minimalist_grammar.MinimalistGrammarTree import MinimalistGrammarTree

# Kayne
# 5.1.1 - HI
with open("output/logs/General Case/01 - log_2017_05_10__02_40_42 - Kayne, Head-initial, PP & CP.txt", "r") as f:
    a = f.readline().split(": ")
    INPUT_511 = ast.literal_eval(a[2])
# page 45
LEXICON_511 = [MinimalistGrammarTree(tree) for tree in [
    "[>@: DP =DP -O]s", "[>@: IP =VP =DP]s", "[>@: VP =PP =VP]s", "[>@: IP =IP -Comp]s",
    "[>Jerry: DP]s", "[>George: DP]s", "[>Elaine: DP]s", "[>Kramer: DP]s",
    "[>ran: VP]s", "[>walked: VP]s", "[>read: VP]s", "[>wrote: VP]s",
    "[>liked: VP =DP]s", "[>saw: VP =DP]s", "[>loved: VP =DP]s", "[>hated: VP =DP]s",
    "[>with: PP =DP]s", "[>by: PP =DP]s", "[>above: PP =DP]s", "[>under: PP =DP]s",
    "[>that: CP =IP]s",
    "[>knows: VP =CP]s", "[>says: VP =CP]s", "[>thinks: VP =CP]s", "[>assumes: VP =CP]s"]]
GRAMMAR_511 = MinimalistGrammar(LEXICON_511)

# 5.1.2 - HF
with open("output/logs/General Case/02 - log_2017_05_10__02_57_53 - Kayne, Head-final, PP & CP.txt", "r") as f:
    a = f.readline().split(": ")
    INPUT_512 = ast.literal_eval(a[2])
# page 46
LEXICON_512 = [MinimalistGrammarTree(tree) for tree in [
    "[>@: DP =DP -O]s", "[>@: IP =VP =DP]s", "[>@: VP =PP =VP]s", "[>@: IP =IP -Comp]s",
    "[>Jerry: DP]s", "[>George: DP]s", "[>Elaine: DP]s", "[>Kramer: DP]s",
    "[>ran: VP]s", "[>walked: VP]s", "[>read: VP]s", "[>wrote: VP]s",
    "[>liked: VP =DP +O]s", "[>saw: VP =DP +O]s", "[>loved: VP =DP +O]s", "[>hated: VP =DP +O]s",
    "[>with: PP =DP +O]s", "[>by: PP =DP +O]s", "[>above: PP =DP +O]s", "[>under: PP =DP +O]s",
    "[>that: CP =IP +Comp -Oc]s",
    "[>knows: VP =CP +Oc]s", "[>says: VP =CP +Oc]s", "[>thinks: VP =CP +Oc]s", "[>assumes: VP =CP +Oc]s"]]
GRAMMAR_512 = MinimalistGrammar(LEXICON_512)

# 5.1.3 - MC
with open("output/logs/General Case/03 - log_2017_05_10__03_54_20 - Kayne, Mixed-category, PP & CP.txt", "r") as f:
    a = f.readline().split(": ")
    INPUT_513 = ast.literal_eval(a[2])
LEXICON_513 = [MinimalistGrammarTree(tree) for tree in [
]]
GRAMMAR_513 = MinimalistGrammar(LEXICON_513)

# 5.1.4 - MW
with open("output/logs/General Case/04 - log_2017_05_10__06_09_15 - Kayne, Mixed-word, PP & CP.txt", "r") as f:
    a = f.readline().split(": ")
    INPUT_514 = ast.literal_eval(a[2])
LEXICON_514 = [MinimalistGrammarTree(tree) for tree in [
]]
GRAMMAR_514 = MinimalistGrammar(LEXICON_514)
