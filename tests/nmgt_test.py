from minimalist_grammar.MinimalistGrammarTree import MinimalistGrammarTree
from minimalist_grammar.NumberMinimalistGrammarTree import *


def test_actions():
    print("\nMerge-1")
    tree1 = MinimalistGrammarTree("[every:=n d -case]s")
    tree2 = MinimalistGrammarTree("[man:n]s")
    merged = tree1.merge(tree2)

    print("Tree 1:", tree1)
    print("Tree 2:", tree2)
    print("Merged:", merged)

    print("\nMerge-2")
    tree1 = MinimalistGrammarTree("[s1:=a b, s2 s3:-f1]c")
    tree2 = MinimalistGrammarTree("[t1:a]s")
    merged = tree1.merge(tree2)

    print("Tree 1:", tree1)
    print("Tree 2:", tree2)
    print("Merged:", merged)

    print("\nMerge-3")
    tree1 = MinimalistGrammarTree("[kiss:=d vt -v]s")
    tree2 = MinimalistGrammarTree("[every girl:d -case]c")
    merged = tree1.merge(tree2)

    print("Tree 1:", tree1)
    print("Tree 2:", tree2)
    print("Merged:", merged)

    print("\nMove-1:")
    tree = MinimalistGrammarTree("[e:+k =d pred, praise:-v, Lavinia:-k]c")
    moved = tree.move()
    print("Tree:", tree)
    print("Moved:", moved)

    print("\nMove-2:")
    tree = MinimalistGrammarTree("[s1:+f1 a, s2 s3: -f1 -f2]c")
    moved = tree.move()
    print("Tree:", tree)
    print("Moved:", moved)


def linguistic_example():
    tree_23 = MinimalistGrammarTree("[Lavinia:d -k]s")
    tree_24 = MinimalistGrammarTree("[Titus:d -k]s")
    tree_25 = MinimalistGrammarTree("[praise:=d vt -v]s")
    tree_26 = MinimalistGrammarTree("[s:=pred +v +k i]s")
    tree_27 = MinimalistGrammarTree("[e:=i c]s")
    tree_28 = MinimalistGrammarTree("[e:=vt +k =d pred]s")

    tree_29 = tree_25.merge(tree_23)
    print(tree_29)
    tree_30 = tree_28.merge(tree_29)
    print(tree_30)
    tree_31 = tree_30.move()
    print(tree_31)
    tree_32 = tree_31.merge(tree_24)
    print(tree_32)
    tree_33 = tree_26.merge(tree_32)
    print(tree_33)
    tree_34 = tree_33.move()
    print(tree_34)
    tree_35 = tree_34.move()
    print(tree_35)
    tree_36 = tree_27.merge(tree_35)
    print(tree_36)


def abstract_example():
    tree_37 = MinimalistGrammarTree("[@: c]s")
    tree_38 = MinimalistGrammarTree("[@: =a +d +b +a c]s")
    tree_39 = MinimalistGrammarTree("[a: =b a -a]s")
    tree_40 = MinimalistGrammarTree("[b:=d b -b]s")
    tree_41 = MinimalistGrammarTree("[d: d -d]s")
    tree_42 = MinimalistGrammarTree("[a:=b +a a -a]s")
    tree_43 = MinimalistGrammarTree("[b:=d +b b -b]s")
    tree_44 = MinimalistGrammarTree("[d:=a +d d -d]s")

    tree_45 = tree_40.merge(tree_41)
    print("45:", tree_45)
    tree_46 = tree_39.merge(tree_45)
    print("46:", tree_46)
    tree_47 = tree_44.merge(tree_46)
    print("47:", tree_47)
    tree_48 = tree_47.move()
    print("48:", tree_48)
    tree_49 = tree_43.merge(tree_48)
    print("49:", tree_49)
    tree_50 = tree_49.move()
    print("50:", tree_50)
    tree_51 = tree_42.merge(tree_50)
    print("51:", tree_51)
    tree_52 = tree_51.move()
    print("52:", tree_52)
    tree_53 = tree_38.merge(tree_52)
    print("53:", tree_53)
    tree_54 = tree_53.move()
    print("54:", tree_54)
    tree_55 = tree_54.move()
    print("55:", tree_55)
    tree_56 = tree_55.move()
    print("56:", tree_56)


if __name__ == '__main__':
    a = NumberMinimalistGrammarTree([NumberMinimalistGrammarNode((0, 1), 0, [1], [], [])], TYPE_SIMPLE)
    b = NumberMinimalistGrammarTree([NumberMinimalistGrammarNode((1, 2), 1, [], [], [])], TYPE_SIMPLE)
    print(a.merge(b))
