from defexpand import infoclass
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import nltk.tag
from unidecode import unidecode

ontology = infoclass.get_info_ontology()
lemmatizer = WordNetLemmatizer()


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


def intersect_ordered(first, second):
    """Finds intersection of two lists, preserving order of first"""
    _auxset = set(second)
    return [x for x in first if x in _auxset]


def similarity_between(infobox_first, infobox_second):
    """Gets raw data about the similarity of two infoboxes from
    DBpedia Ontology
    """
    _above_first = ontology.classes_above_infobox(infobox_first)
    _above_second = ontology.classes_above_infobox(infobox_second)

    # get lowest shared class in DBpedia ontology tree
    shared_dbpedia_class = intersect_ordered(_above_first, _above_second)[0]

    # count classes above the infobox's immediate class
    # (if they are the same, counts will =0)
    count_from_first = _above_first.index(shared_dbpedia_class)
    count_from_second = _above_second.index(shared_dbpedia_class)

    # counts includes the root (if they only share root, then count_from_root=0)
    _above_shared = ontology.classes_above(shared_dbpedia_class)
    count_from_root = len(_above_shared) - 1 # so root = 0

    return [shared_dbpedia_class, count_from_root,
            count_from_first, count_from_second]


def similar_enough(infobox_first,
                   infobox_second,
                   min_from_root = 1,
                   max_from_either_infobox = 2):
                   # special_cases = True):
    _similarity_between = similarity_between(infobox_first, infobox_second)
    [shared_dbpedia_class, count_from_root,
     count_from_first, count_from_second] = _similarity_between

    # very_general_classes = ['Agent', 'Event', 'Place']
    # _is_special = shared_dbpedia_class in very_general_classes

    # if max_from_either_infobox == 2 and _is_special and special_cases:
    #    max_from_either_infobox = 3

    within_max_from_infobox = (count_from_first <= max_from_either_infobox and
                               count_from_second <= max_from_either_infobox)

    return within_max_from_infobox and count_from_root >= min_from_root

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        raise KeyError("Treebank contains no such tag: " + treebank_tag)


def auto_lemmatize(word):
    # TODO: this handles single words nicely, but cannot do 'maintained by'
    tagged = nltk.pos_tag([word])[0]
    treebank_pos = tagged[1]
    return lemmatizer.lemmatize(word, get_wordnet_pos(treebank_pos))


# def get_synonyms(object_class, property, value_class):
#     # stub
