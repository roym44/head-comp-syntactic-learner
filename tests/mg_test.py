from functools import cmp_to_key
from minimalist_grammar.MinimalistGrammar import get_grammar_from_string, compare_for_susbtrings

def sort_grammar_string(grammar_string):
    lexicon = get_grammar_from_string(grammar_string).lexicon
    return sorted(lexicon, key=cmp_to_key(compare_for_susbtrings))


if __name__ == '__main__':
    grammar_string = '''
[[>@: IP =VP =DP]s, [>@: VP =PP =VP]s, [>@: DP =DP -O]s, [>@: IP =IP -Comp]s, [>ran: VP]s, [>walked: VP]s, [>read: VP]s, [>Elaine: DP]s, [>George: DP]s, [>Kramer: DP]s, [>Jerry: DP]s, [>saw: VP =DP]s, [>liked: VP =DP]s, [>assumes: VP =CP]s, [>knows: VP =CP]s, [>says: VP =CP]s, [>thinks: VP =CP]s, [<with: PP =DP]s, [<under: PP =DP]s, [>wrote: VP]s, [>that: CP =IP]s, [<by: PP =DP]s, [<above: PP =DP]s, [<loved: VP =DP]s, [<hated: VP =DP]s]
'''
    print(sort_grammar_string(grammar_string))
