import random

# The grammar here should be [name: NP]s, [verb: VP =NP =NP]s
NORMAL = "Pennypacker thinks that Newman writes#Kramer writes#Newman assumes that Vandalay writes#Newman loves Vandalay#Newman knows that Newman walks by Jerry#Newman walks#Babu runs#George loves Babu#Jerry says that Elaine walks by Kramer#Kramer thinks that Jerry thinks that Vandalay writes#Newman runs with Newman#Pennypacker walks#Vandalay thinks that Elaine writes with Vandalay with Elaine#Babu reads above Jerry#Pennypacker walks by Babu#George runs with Pennypacker#Pennypacker reads by Pennypacker#Pennypacker runs#Babu says that Pennypacker sees Vandalay above Kramer#Kramer hates Jerry#Vandalay writes above George#Vandalay assumes that Newman hates Pennypacker with Elaine#Pennypacker loves Elaine by Elaine#Vandalay hates Babu#Newman thinks that Jerry sees Babu#Vandalay says that Newman knows that Elaine knows that George likes Kramer above Jerry with Kramer above Vandalay#Babu sees Jerry#George loves Elaine by Newman#Kramer thinks that George loves Newman with George above Elaine#Elaine reads by Newman#Jerry assumes that Newman runs above Vandalay#Newman thinks that Jerry walks by Elaine#Jerry loves Jerry#Pennypacker sees Jerry#Jerry runs with Babu#George runs#Kramer says that George says that Elaine loves Babu with Kramer above Vandalay with Elaine#Pennypacker runs#Babu assumes that Jerry runs#Babu walks#George thinks that Newman assumes that Jerry reads by Babu#George thinks that Vandalay likes Elaine with George#Babu runs#George runs above Jerry#Elaine runs above Elaine#Elaine thinks that Kramer thinks that Pennypacker assumes that Pennypacker walks above Pennypacker by Newman with George#George walks#George walks#Jerry likes George#Newman assumes that Babu sees Elaine by George#"
SEUSS = ""
SIMPLE = "Vandalay runs#George loves Vandalay#Newman writes by Elaine#Kramer likes Babu with Elaine#Vandalay likes George by Newman#Kramer runs with Newman#Newman likes Vandalay above Jerry#Elaine writes#Pennypacker hates Kramer above Pennypacker#Jerry hates Vandalay#Kramer loves Babu above Babu#Elaine likes Jerry with Vandalay#Kramer likes George#Babu likes George#Vandalay hates Babu above Kramer#George walks#Elaine loves Elaine#Newman loves Newman by Babu#Kramer loves Newman by Babu#Elaine loves Elaine#Jerry likes Jerry with Pennypacker#Vandalay sees Babu by Pennypacker#Babu sees Pennypacker#Babu loves Kramer by Jerry#Kramer sees Vandalay#George loves Vandalay#Babu likes Pennypacker#Jerry loves Babu#Vandalay loves Newman by Babu#Newman hates Babu above Newman#Jerry sees George#Elaine hates Newman#Newman hates Elaine#Vandalay loves Babu#Elaine sees Elaine with Elaine#Newman sees Jerry#Jerry likes Vandalay above Jerry#Pennypacker hates Pennypacker above George#Elaine likes Newman#Newman walks with Newman#Jerry sees Pennypacker#Babu loves Jerry above Babu#George sees Elaine#Newman loves George with George#Kramer hates Elaine above Babu#Kramer hates Vandalay above Elaine#Jerry sees Jerry#Jerry loves Elaine#Pennypacker hates Newman#Kramer sees Newman#"
JAPANESE_LIKE = "George writes#Pennypacker reads#Pennypacker writes#Kramer runs#Elaine runs#George runs#Elaine writes#Babu writes#George runs#George walks#Elaine writes#Babu reads#Jerry reads#Babu walks#Elaine runs#Jerry writes#George walks#Kramer reads#Vandalay writes#Kramer writes#Babu reads#George runs#George walks#Vandalay writes#Jerry runs#Vandalay walks#Pennypacker writes#Babu reads#Kramer reads#Elaine walks#Elaine writes#Jerry writes#Babu reads#Newman runs#Elaine runs#Babu walks#Pennypacker walks#Elaine reads#Elaine runs#George runs#Jerry runs#Elaine walks#Jerry reads#Kramer walks#Pennypacker writes#Kramer writes#Babu reads#Pennypacker reads#Babu reads#Kramer runs#"
ENGLISH_LIKE = "Elaine reads#Jerry reads#George walks#Pennypacker runs#Jerry writes#Elaine runs#Pennypacker walks#Pennypacker walks#Jerry writes#Pennypacker runs#Kramer writes#Vandalay reads#George walks#Elaine writes#Jerry writes#Newman walks#Pennypacker writes#Kramer writes#George runs#Babu walks#Babu walks#George walks#George writes#George walks#Elaine writes#George reads#Babu reads#Newman reads#Newman walks#Elaine runs#Babu walks#Newman reads#Newman walks#Kramer runs#Elaine runs#Jerry walks#Vandalay writes#Kramer runs#Elaine walks#George walks#Babu walks#Vandalay walks#Elaine runs#Jerry writes#Elaine reads#Newman reads#Babu reads#George runs#Elaine reads#Newman runs#"

proper_nouns = ["Jerry", "George", "Elaine", "Kramer"]  # , "Vandalay", "Pennypacker", "Babu", "Newman", "Yev", "Mulva"]
# Is that how they're called?
improper_nouns = ["boy", "girl", "dog", "cat"]  # , "man", "woman", "hedgehog", "llama", "postman", "comedian"]
transitive = ["liked", "saw", "loved", "hated"]  # , "hugged", "tickled", "kissed", "found", "punched", "kicked"]
intransitive = ["ran", "walked", "read", "wrote"]  # , "ate", "drank", "slept", "woke", "whistled", "laughed"]
cp_transitive = ["knew", "said", "thought", "assumed"]
prepositions = ["with", "by", "above", "under"]
definite_articles = ["the", "a", "this", "some"]
complementizers = ["that"]
conjunctors = ["and"]  # , "or"]
delimiter = " "


# Headedness is one of ["initial", "final", "category", "word"]
def get_custom_text(size,
                    with_transitive=None,
                    with_dp=None,
                    with_prepositions=None,
                    with_cp=None,
                    with_coordination=False,
                    recursion_depth=0):
    text = ""
    for i in range(size):
        sentence = None
        while sentence is None:
            sentence = generate_customizable_sentence(with_transitive=with_transitive,
                                                      with_prepositions=with_prepositions,
                                                      with_dp=with_dp,
                                                      with_cp=with_cp,
                                                      with_coordination=with_coordination,
                                                      recursion_depth=recursion_depth)
        text += sentence
        text += "#"
    return text


def get_japanese_like_text(size):
    text = ""
    for i in range(size):
        sentence = None
        while sentence is None:
            sentence = generate_customizable_sentence(head_initial=False,
                                                      with_transitive=True,
                                                      with_prepositions=False,
                                                      with_dp=True,
                                                      recursion_depth=0)

        text += sentence
        text += "#"

    return text


def get_english_like_text(size):
    text = ""
    for i in range(size):
        sentence = None
        while sentence is None:
            sentence = generate_customizable_sentence(head_initial=True,
                                                      with_transitive=True,
                                                      with_prepositions=False,
                                                      with_dp=True,
                                                      recursion_depth=0)

        text += sentence
        text += "#"
    return text


# Each possible head is either "initial", "final" or "mixed".
# "mixed" means that the first two words in that head will be head-initial and the rest will be head-final.
def generate_customizable_sentence(with_transitive=None,
                                   with_prepositions=None,
                                   with_dp=None,
                                   with_cp=None,
                                   with_coordination=False,
                                   recursion_depth=0):
    for type in [with_transitive, with_prepositions, with_dp, with_cp]:
        assert (type in ["initial", "final", "mixed", None])

    sentence = ""
    nouns = sorted(proper_nouns)
    if with_dp:
        for noun in improper_nouns:
            for da in definite_articles:
                if with_dp == "initial" or (with_dp == "mixed" and da in definite_articles[:2]):
                    nouns.append(delimiter.join([da, noun]))
                else:
                    nouns.append(delimiter.join([noun, da]))
    sentence += random.choice(nouns)
    sentence += delimiter
    # Coordination of the subject.
    if with_coordination and random.choice([True, False]):
        sentence += random.choice(conjunctors) + delimiter + random.choice(nouns) + delimiter

    # This just makes a copy of the list so it doesn't get changed.
    verbs = sorted(intransitive)
    if with_transitive:
        verbs += transitive
    if with_cp and recursion_depth > 0:
        verbs += cp_transitive

    # Doing it twice for coordination.
    for i in range(2):
        verb = random.choice(verbs)
        if verb in intransitive:
            sentence += verb
        if verb in transitive:
            # Coordination of the object.
            if with_coordination and random.choice([True, False]):
                object = random.choice(nouns) + delimiter + random.choice(conjunctors) + delimiter + random.choice(
                    nouns)
            else:
                object = random.choice(nouns)

            if with_transitive == "final" or (with_transitive == "mixed" and verb not in transitive[:2]):
                sentence += object
                sentence += delimiter
                sentence += verb
            else:
                sentence += verb
                sentence += delimiter
                sentence += object

        if verb in cp_transitive:
            cp = ''
            # Doing it twice for coordination.
            for j in range(2):
                comp = random.choice(complementizers)
                new_sentence = None
                while new_sentence is None:
                    new_sentence = generate_customizable_sentence(with_transitive=with_transitive,
                                                                  with_prepositions=with_prepositions,
                                                                  with_dp=with_dp,
                                                                  with_cp=with_cp,
                                                                  with_coordination=with_coordination,
                                                                  recursion_depth=recursion_depth - 1)

                # The coordination of the IP within the CP is done by the coordination of the whole IP in the recursive call.
                # Since there is only one complementizer there is no sense in making it "mixed".
                if with_cp == "initial":
                    cp += delimiter.join([comp, new_sentence])
                else:
                    cp += delimiter.join([new_sentence, comp])

                # Coordination of the object (CP).
                if False:
                    # if with_coordination and j == 0 and random.choice([True, False]):
                    cp += delimiter + random.choice(conjunctors) + delimiter
                else:
                    # Only run the loop once.
                    break

            # Making the cp verbs mixed too makes things difficult so we won't do it.
            if with_transitive == "initial" or with_transitive == "mixed":
                sentence += delimiter.join([verb, cp])
            else:
                sentence += delimiter.join([cp, verb])

        if with_prepositions and random.choice([True, False]):
            # Doing it twice for coordination.
            for k in range(2):
                preposition = random.choice(prepositions)

                # Coordination of the complement.
                if with_coordination and random.choice([True, False]):
                    complement = random.choice(nouns) + delimiter + random.choice(
                        conjunctors) + delimiter + random.choice(nouns)
                else:
                    complement = random.choice(nouns)

                if with_prepositions == "initial" or (with_prepositions == "mixed" and preposition in prepositions[:2]):
                    sentence += delimiter.join(['', preposition, complement])
                else:
                    sentence += delimiter.join(['', complement, preposition])

                # Coordination of the PP.
                if False:
                    # if with_coordination and k == 0 and random.choice([True, False]):
                    sentence += delimiter + random.choice(conjunctors)
                else:
                    # Only run the loop once.
                    break

        # Coordination of the VP + PP.
        if False:
            # if with_coordination and i == 0 and random.choice([True, False]):
            sentence += delimiter + random.choice(conjunctors) + delimiter
        else:
            # Only run the loop once.
            break

    if False:
        # if with_coordination and random.choice([True, False]) and recursion_depth == 0:
        new_sentence = None
        while new_sentence is None:
            new_sentence = generate_customizable_sentence(with_transitive=with_transitive,
                                                          with_prepositions=with_prepositions,
                                                          with_dp=with_dp,
                                                          with_cp=with_cp,
                                                          with_coordination=False,
                                                          # I only allow one coordination per sentence.
                                                          recursion_depth=recursion_depth)

        sentence += delimiter + random.choice(conjunctors) + delimiter + new_sentence

    # I only allow two coordination per sentence.
    coordinations = 0
    for word in sentence.split(delimiter):
        if word in conjunctors:
            coordinations += 1
    if coordinations > 2:
        return None

    if len(sentence.split()) > 8:
        return None
    return sentence


# This generates sentences of the form N V N.
def get_normal_text(size):
    text = ""
    for i in range(size):
        sentence = generate_sentence()

        text += sentence
        text += "#"

    return text


def get_simple_text(size):
    text = ""
    for i in range(size):
        sentence = generate_sentence(with_recursion=False)

        text += sentence
        text += "#"

    return text


def generate_sentence(with_transitive=True, with_recursion=True, with_prepositions=True):
    sentence = ""
    sentence += random.choice(nouns)
    sentence += " "

    verbs = intransitive
    if with_transitive:
        verbs += transitive
    if with_recursion:
        verbs += cp_transitive

    verb = random.choice(verbs)
    sentence += verb
    if verb in transitive:
        sentence += " "
        sentence += random.choice(nouns)
    if verb in cp_transitive:
        sentence += " that " + generate_sentence()
    if random.choice([True, False]):
        sentence += ' %s %s' % (random.choice(prepositions), random.choice(nouns))
    return sentence


def write_text_to_const(name, text):
    filename = __file__
    if filename.endswith('c'):
        filename = filename[:-1]
    code = open(filename, 'r').read()
    const_string = name + ' = "'
    index_of_text = code.index(const_string) + len(const_string)
    index_of_closing_quote = code.index('"', index_of_text)
    new_code = code[:index_of_text] + text + code[index_of_closing_quote:]
    file = open(filename, 'w')
    file.write(new_code)
    file.close()


if __name__ == '__main__':
    """
    TODO: first impressions:
    - all the consts at the top of the file are not used in the code, maybe we can remove them
    - only one function here is used outside - get_custom_text, maybe we can remove the rest
    - nouns in the code actually refer to proper_nouns list
    """
    text = get_english_like_text(50)
    write_text_to_const("ENGLISH_LIKE", text)
