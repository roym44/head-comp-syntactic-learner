from minimalist_grammar.MinimalistGrammar import MinimalistGrammar
from minimalist_grammar.MinimalistGrammarTree import MinimalistGrammarTree

LINGUISTIC_LEXICON = [
    MinimalistGrammarTree("[>Lavinia:d -k]s"),
    MinimalistGrammarTree("[>Titus:d -k]s"),
    MinimalistGrammarTree("[>praise:=d vt -v]s"),
    MinimalistGrammarTree("[>s:=pred +v +k i]s"),
    MinimalistGrammarTree("[>@:=i IP]s"),
    MinimalistGrammarTree("[>@:=vt +k =d pred]s")
    ]
LINGUISTIC_GRAMMAR = MinimalistGrammar(LINGUISTIC_LEXICON)

ABSTRACT_LEXICON = [
    MinimalistGrammarTree("[>@: IP]s"),
    MinimalistGrammarTree("[>@: =a +d +b +a IP]s"),
    MinimalistGrammarTree("[>a: =b a -a]s"),
    MinimalistGrammarTree("[>b:=d b -b]s"),
    MinimalistGrammarTree("[>d: d -d]s"),
    MinimalistGrammarTree("[>a:=b +a a -a]s"),
    MinimalistGrammarTree("[>b:=d +b b -b]s"),
    MinimalistGrammarTree("[>d:=a +d d -d]s"),
    ]
ABSTRACT_GRAMMAR = MinimalistGrammar(ABSTRACT_LEXICON)

STABLER_LEXICON = [
    MinimalistGrammarTree("[>@:=v IP]s"),
    MinimalistGrammarTree("[>@:=v +wh IP]s"),
    MinimalistGrammarTree("[>knows:=IP =d v]s"),
    MinimalistGrammarTree("[>says:=IP =d v]s"),
    MinimalistGrammarTree("[>prefers:=d =d v]s"),
    MinimalistGrammarTree("[>drinks:=d =d v]s"),
    MinimalistGrammarTree("[>king:n]s"),
    MinimalistGrammarTree("[>queen:n]s"),
    MinimalistGrammarTree("[>wine:n]s"),
    MinimalistGrammarTree("[>beer:n]s"),
    MinimalistGrammarTree("[>the:=n d]s"),
    MinimalistGrammarTree("[>which:=n d -wh]s")
    ]
STABLER_GRAMMAR = MinimalistGrammar(STABLER_LEXICON)

ENGLISH_LEXICON = [
    MinimalistGrammarTree("[>@:IP =VP =DP]s"),
    
    MinimalistGrammarTree("[>walked:VP]s"),
    MinimalistGrammarTree("[>ran:VP]s"),
    MinimalistGrammarTree("[>read:VP]s"),
    MinimalistGrammarTree("[>wrote:VP]s"),
    
    MinimalistGrammarTree("[>@:VP =PP =VP]s"),
    
    MinimalistGrammarTree("[>that:CP =IP]s"),
    
    MinimalistGrammarTree("[>liked:VP =DP]s"),
    MinimalistGrammarTree("[>saw:VP =DP]s"),
    MinimalistGrammarTree("[>loved:VP =DP]s"),
    MinimalistGrammarTree("[>hated:VP =DP]s"),
    
    MinimalistGrammarTree("[>knows:VP =CP]s"),
    MinimalistGrammarTree("[>says:VP =CP]s"),
    MinimalistGrammarTree("[>thinks:VP =CP]s"),
    MinimalistGrammarTree("[>assumes:VP =CP]s"),
    
    MinimalistGrammarTree("[>with:PP =DP]s"),
    MinimalistGrammarTree("[>by:PP =DP]s"),
    MinimalistGrammarTree("[>above:PP =DP]s"),
    MinimalistGrammarTree("[>under:PP =DP]s"),
    
    # MinimalistGrammarTree("[>the:DP =NP]s"),
    # MinimalistGrammarTree("[>a:DP =NP]s"),
    # MinimalistGrammarTree("[>some:DP =NP]s"),
    # MinimalistGrammarTree("[>this:DP =NP]s"),
    
    # MinimalistGrammarTree("[>boy:NP]s"),
    # MinimalistGrammarTree("[>girl:NP]s"),
    # MinimalistGrammarTree("[>cat:NP]s"),
    # MinimalistGrammarTree("[>dog:NP]s"),
    
    MinimalistGrammarTree("[>Jerry:DP]s"),
    MinimalistGrammarTree("[>George:DP]s"),
    MinimalistGrammarTree("[>Elaine:DP]s"),
    MinimalistGrammarTree("[>Kramer:DP]s"),
    
    MinimalistGrammarTree("[>and:DP =DP =DP]s"),
    MinimalistGrammarTree("[>and:VP =VP =VP]s"),
    MinimalistGrammarTree("[>and:PP =PP =PP]s"),
    MinimalistGrammarTree("[>and:CP =CP =CP]s"),
    MinimalistGrammarTree("[>and:IP =IP =IP]s"),
    ]
ENGLISH_GRAMMAR = MinimalistGrammar(ENGLISH_LEXICON)

HEAD_FINAL_LEXICON = [
    # Absolute:
    MinimalistGrammarTree("[>@:IP =VP =DP]s"),
    
    MinimalistGrammarTree("[>walked:VP]s"),
    MinimalistGrammarTree("[>ran:VP]s"),
    MinimalistGrammarTree("[>read:VP]s"),
    MinimalistGrammarTree("[>wrote:VP]s"),
    
    MinimalistGrammarTree("[>Jerry:DP]s"),
    MinimalistGrammarTree("[>George:DP]s"),
    MinimalistGrammarTree("[>Elaine:DP]s"),
    MinimalistGrammarTree("[>Kramer:DP]s"),
    
    MinimalistGrammarTree("[>@:VP =PP =VP]s"),

    MinimalistGrammarTree("[>@:DP =DP -O]s"),    
    MinimalistGrammarTree("[>@:IP =IP -Comp]s"),
    
    MinimalistGrammarTree("[>that:CP =IP +Comp -Oc]s"),
    
    MinimalistGrammarTree("[>liked:VP =DP +O]s"),
    MinimalistGrammarTree("[>saw:VP =DP +O]s"),
    MinimalistGrammarTree("[>loved:VP =DP +O]s"),
    MinimalistGrammarTree("[>hated:VP =DP +O]s"),
    
    MinimalistGrammarTree("[>knows:VP =CP +Oc]s"),
    MinimalistGrammarTree("[>says:VP =CP +Oc]s"),
    MinimalistGrammarTree("[>thinks:VP =CP +Oc]s"),
    MinimalistGrammarTree("[>assumes:VP =CP +Oc]s"),
    
    MinimalistGrammarTree("[>with:PP =DP +O]s"),
    MinimalistGrammarTree("[>by:PP =DP +O]s"),
    MinimalistGrammarTree("[>above:PP =DP +O]s"),
    MinimalistGrammarTree("[>under:PP =DP +O]s"),
    
    MinimalistGrammarTree("[>and:DP =DP =DP]s"),
    MinimalistGrammarTree("[>and:VP =VP =VP]s"),
    MinimalistGrammarTree("[>and:PP =PP =PP]s"),
    MinimalistGrammarTree("[>and:CP =CP =CP]s"),
    MinimalistGrammarTree("[>and:IP =IP =IP]s"),
    ]
HEAD_FINAL_GRAMMAR = MinimalistGrammar(HEAD_FINAL_LEXICON)
