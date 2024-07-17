import random

proper_nouns = ["Jerry", "George", "Elaine", "Kramer"]  # , "Vandalay", "Pennypacker", "Babu", "Newman", "Yev", "Mulva"]
# Is that how they're called?
improper_nouns = ["boy", "girl", "dog", "cat"]  # , "man", "woman", "hedgehog", "llama", "postman", "comedian"]
transitive = ["liked", "saw", "loved", "hated"]  # , "hugged", "tickled", "kissed", "found", "punched", "kicked"]
intransitive = ["ran", "walked", "read", "wrote"]  # , "ate", "drank", "slept", "woke", "whistled", "laughed"]
# at some point he switched cp_transitive verbs to past, they were in present tense before
# cp_transitive = ["knew", "said", "thought", "assumed"]
cp_transitive = ["knows", "says", "thinks", "assumes"]
prepositions = ["with", "by", "above", "under"]
definite_articles = ["the", "a", "this", "some"]
complementizers = ["that"]
# NOTE: this is added only if with_coordination is True
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
        # TODO: replace += with extends? or something else that adds to the same list, doesn't create a new list in memory every time
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
