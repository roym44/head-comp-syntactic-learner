from MinimalistGrammar import MinimalistGrammar
from MinimalistGrammarTree import MinimalistGrammarTree

KAYNE_LEXICON_WITH_HACK = [
    # Absolute:
    MinimalistGrammarTree("[>@:IP =VP =DP]s"),
    
    MinimalistGrammarTree("[>*:VP]s"),
    
    MinimalistGrammarTree("[>@:VP =PP =VP]s"),
    
    # Head initial:
    MinimalistGrammarTree("[>*:CP =IP]s"),
    
    MinimalistGrammarTree("[>*:VP =DP]s"),
    MinimalistGrammarTree("[>*:VP =CP]s"),
    
    MinimalistGrammarTree("[>*:PP =DP]s"),
    
    MinimalistGrammarTree("[>*:DP]s"),
    
    # Head Final:
    MinimalistGrammarTree("[>*:CP =IP +Comp, @: -Comp]c"),
    
    MinimalistGrammarTree("[>*:VP =DP +O, @: -O]c"),
    MinimalistGrammarTree("[>*:VP =CP +O, @: -O]c"),
    
    MinimalistGrammarTree("[>@:VP =VP =PP]s"),
    MinimalistGrammarTree("[>*:PP =DP +O, @: -O]c"),
    ]
KAYNE_GRAMMAR_WITH_HACK = MinimalistGrammar(KAYNE_LEXICON_WITH_HACK)

KAYNE_LEXICON_WITH_EMPTY_DP = [
    # Absolute:
    MinimalistGrammarTree("[>@:IP =VP =DP]s"),
    
    MinimalistGrammarTree("[>*:VP]s"),
    MinimalistGrammarTree("[>*:DP]s"),
    
    # Head initial:
    MinimalistGrammarTree("[>*:CP =IP]s"),
    
    MinimalistGrammarTree("[>*:VP =DP]s"),
    MinimalistGrammarTree("[>*:VP =CP]s"),
    
    MinimalistGrammarTree("[>@:VP =PP =VP]s"),
    MinimalistGrammarTree("[>*:PP =DP]s"),
    
    # Head Final:
    MinimalistGrammarTree("[>@:DP =DP -O]s"),    
    MinimalistGrammarTree("[>@:IP =IP -Comp]s"),
    
    MinimalistGrammarTree("[>*:CP =IP +Comp -Oc]s"),
    
    MinimalistGrammarTree("[>*:VP =DP +O]s"),
    MinimalistGrammarTree("[>*:VP =CP +Oc]s"),
    
    MinimalistGrammarTree("[>*:PP =DP +O]s"),
    
    MinimalistGrammarTree("[>*:DP =DP =DP]s"),
    # MinimalistGrammarTree("[>*:VP =VP =VP]s"),
    # MinimalistGrammarTree("[>*:PP =PP =PP]s"),
    # MinimalistGrammarTree("[>*:CP =CP =CP]s"),
    # MinimalistGrammarTree("[>*:IP =IP =IP]s"),
    ]
KAYNE_GRAMMAR_WITH_EMPTY_DP = MinimalistGrammar(KAYNE_LEXICON_WITH_EMPTY_DP)

KAYNE_LEXICON_WITH_TWO_DP = [
    # Absolute:
    MinimalistGrammarTree("[>@:IP =VP =DP]s"),
    # MinimalistGrammarTree("[@:IP =VP =DP +O]s"),
    
    MinimalistGrammarTree("[>*:VP]s"),
    
    MinimalistGrammarTree("[>@:VP =PP =VP]s"),
    
    # Head initial:
    # MinimalistGrammarTree("[>*:CP =IP]s"),
    
    MinimalistGrammarTree("[>*:VP =DP]s"),
    # MinimalistGrammarTree("[>*:VP =CP]s"),
    
    MinimalistGrammarTree("[>*:PP =DP]s"),
    
    MinimalistGrammarTree("[>*:DP]s"),
    
    # Head Final:
    # MinimalistGrammarTree("[>@:IP =IP -Comp]s"),
    # MinimalistGrammarTree("[>*:CP =IP +Comp]s"),
    
    MinimalistGrammarTree("[>*:VP =DP +O]s"),
    # MinimalistGrammarTree("[>*:VP =CP +O]s"),
    
    MinimalistGrammarTree("[>@:VP =VP =PP]s"),
    MinimalistGrammarTree("[>*:PP =DP +O]s"),
    
    # MinimalistGrammarTree("[>@:DP =DP -O]s"),
    
    MinimalistGrammarTree("[>*:DP -O]s"),
    ]
KAYNE_GRAMMAR_WITH_TWO_DP = MinimalistGrammar(KAYNE_LEXICON_WITH_TWO_DP)

KAYNE_LEXICON_WITH_ONLY_LICENSEE_DP = [
    # Absolute:
    MinimalistGrammarTree("[>@:IP =VP =DP]s"),
    MinimalistGrammarTree("[>@:IP =VP =DP +O]s"),
    
    MinimalistGrammarTree("[>*:VP]s"),
    
    MinimalistGrammarTree("[>@:VP =PP =VP]s"),
    
    # Head initial:
    # MinimalistGrammarTree("[>*:CP =IP]s"),
    
    MinimalistGrammarTree("[>*:VP =DP]s"),
    # MinimalistGrammarTree("[>*:VP =CP]s"),
    
    MinimalistGrammarTree("[>*:PP =DP]s"),
    
    MinimalistGrammarTree("[>*:DP]s"),
    
    # Head Final:
    # MinimalistGrammarTree("[>@:IP =IP -Comp]s"),
    # MinimalistGrammarTree("[>*:CP =IP +Comp]s"),
    
    MinimalistGrammarTree("[>*:VP =DP +O]s"),
    # MinimalistGrammarTree("[>*:VP =CP +O]s"),
    
    MinimalistGrammarTree("[>@:VP =VP =PP]s"),
    MinimalistGrammarTree("[>*:PP =DP +O]s"),
    
    # MinimalistGrammarTree("[>@:DP =DP -O]s"),
    
    MinimalistGrammarTree("[>*:DP -O]s"),
    ]
KAYNE_GRAMMAR_WITH_ONLY_LICENSEE_DP = MinimalistGrammar(KAYNE_LEXICON_WITH_ONLY_LICENSEE_DP)

