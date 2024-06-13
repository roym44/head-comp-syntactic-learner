from minimalist_grammar.MinimalistGrammar import MinimalistGrammar
from minimalist_grammar.MinimalistGrammarTree import MinimalistGrammarTree

KAYNE_LEXICON_WITH_HACK = [MinimalistGrammarTree(tree) for tree in [
    # Absolute:
    "[>@:IP =VP =DP]s", "[>*:VP]s", "[>@:VP =PP =VP]s",
    # Head initial:
    "[>*:CP =IP]s", "[>*:VP =DP]s", "[>*:VP =CP]s", "[>*:PP =DP]s", "[>*:DP]s",
    # Head Final:
    "[>*:CP =IP +Comp, @: -Comp]c", "[>*:VP =DP +O, @: -O]c", "[>*:VP =CP +O, @: -O]c",
    "[>@:VP =VP =PP]s", "[>*:PP =DP +O, @: -O]c"]]
KAYNE_GRAMMAR_WITH_HACK = MinimalistGrammar(KAYNE_LEXICON_WITH_HACK)

# NEW
KAYNE_LEXICON_WITH_EMPTY_DP_NO_CO = [MinimalistGrammarTree(tree) for tree in [
    # Absolute:
    "[>@:IP =VP =DP]s", "[>*:VP]s", "[>*:DP]s",
    # Head initial:
    # "[>@:VP =PP =VP]s" = PP to the right of VP
    "[>*:CP =IP]s", "[>*:VP =DP]s", "[>*:VP =CP]s", "[>@:VP =PP =VP]s", "[>*:PP =DP]s",
    # Head Final:
    # "[>*:DP =DP =DP]s", "[>*:VP =VP =VP]s", "[>*:PP =PP =PP]s", "[>*:CP =CP =CP]s", "[>*:IP =IP =IP]s"
    # wrappers for DP, IP
    "[>@:DP =DP -O]s", "[>@:IP =IP -Comp]s", "[>*:CP =IP +Comp -Oc]s", "[>*:VP =DP +O]s", "[>*:VP =CP +Oc]s",
    "[>*:PP =DP +O]s"]]

KAYNE_GRAMMAR_WITH_EMPTY_DP_NO_CO = MinimalistGrammar(KAYNE_LEXICON_WITH_EMPTY_DP_NO_CO)

KAYNE_LEXICON_WITH_EMPTY_DP = KAYNE_LEXICON_WITH_EMPTY_DP_NO_CO + [MinimalistGrammarTree("[>*:DP =DP =DP]s")]
KAYNE_GRAMMAR_WITH_EMPTY_DP = MinimalistGrammar(KAYNE_LEXICON_WITH_EMPTY_DP)

KAYNE_LEXICON_WITH_TWO_DP = [MinimalistGrammarTree(tree) for tree in [
    # Absolute:
    # "[@:IP =VP =DP +O]s"
    # TODO: does "[>@:VP =PP =VP]s" = PP to the right of VP, really exist?
    "[>@:IP =VP =DP]s", "[>@:IP =VP =DP +O]s", "[>*:VP]s", "[>@:VP =PP =VP]s",
    # Head initial:
    # "[>*:CP =IP]s", "[>*:VP =CP]s"
    "[>*:VP =DP]s", "[>*:PP =DP]s", "[>*:DP]s",
    # Head Final:
    # "[>@:IP =IP -Comp]s", "[>*:CP =IP +Comp]s", "[>*:VP =CP +O]s", "[>@:DP =DP -O]s"
    "[>*:VP =DP +O]s", "[>@:VP =VP =PP]s", "[>*:PP =DP +O]s", "[>*:DP -O]s"]]
KAYNE_GRAMMAR_WITH_TWO_DP = MinimalistGrammar(KAYNE_LEXICON_WITH_TWO_DP)

KAYNE_LEXICON_WITH_ONLY_LICENSEE_DP = [MinimalistGrammarTree(tree) for tree in [
    # Absolute:
    "[>@:IP =VP =DP]s", "[>@:IP =VP =DP +O]s", "[>*:VP]s", "[>@:VP =PP =VP]s",
    # Head initial:
    # "[>*:CP =IP]s", "[>*:VP =CP]s",
    "[>*:VP =DP]s", "[>*:PP =DP]s", "[>*:DP]s",
    # Head Final:
    # "[>@:IP =IP -Comp]s", "[>*:CP =IP +Comp]s", "[>*:VP =CP +O]s", "[>@:DP =DP -O]s"
    "[>*:VP =DP +O]s", "[>@:VP =VP =PP]s", "[>*:PP =DP +O]s", "[>*:DP -O]s"]]
KAYNE_GRAMMAR_WITH_ONLY_LICENSEE_DP = MinimalistGrammar(KAYNE_LEXICON_WITH_ONLY_LICENSEE_DP)
