from nltk.corpus import wordnet as wn
from unidecode import unidecode


def clean_wordnet(word):
    word = unidecode(word)
    word = word.replace('_', ' ')
    word = word.lower()
    return word


def id_synset(primary, keys):
    candidates = [[clean_wordnet(name) for name in synset.lemma_names()]
                  for synset in wn.synsets(primary)]
    if len(candidates) == 0:
        raise KeyError("WordNet contains no synsets for word: " + primary)
    else:
        sublist = [x for x in candidates if keys[0] in x]
        keys.pop(0)             # remove used key
        while len(sublist) > 1 and len(keys) > 0:
            # further narrow down
            sub_sublist = [x for x in sublist if keys[0] in x]
            if len(sub_sublist) > 0:
                sublist = sub_sublist
            keys.pop(0)             # remove used key

        if len(sublist) == 0:
            raise RuntimeError("No synset of '" + primary + "' matches keys")
        if len(sublist) > 1:
            raise RuntimeError("Keys insufficient to uniquely identify synset, "
                               + str(len(sublist)) + " synsets found")
        else:
            return sublist[0]
