from defexpand import infoclass
from nltk.corpus import wordnet as wn
import nltk.tag
from unidecode import unidecode
from wikimap import data, graph
from wikimap.config import DATA_DIRECTORY

ontology = infoclass.get_info_ontology()
master_graph = data.read_graph(DATA_DIRECTORY + "wikimap-live.gpickle")


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
            raise RuntimeError("No synset of <" + primary + "> matches keys")
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

    if _above_first == []:
        raise KeyError("non-existant class: " + infobox_first)
    elif _above_second == []:
        raise KeyError("non-existant class: " + infobox_second)
    else:
        # get lowest shared class in DBpedia ontology tree
        shared_dbpedia_class = intersect_ordered(_above_first, _above_second)[0]

        # count classes above the infobox's immediate class
        # (if they are the same, counts will =0)
        count_from_first = _above_first.index(shared_dbpedia_class)
        count_from_second = _above_second.index(shared_dbpedia_class)

        # counts includes the root (if they only share root, then
        # count_from_root=0)
        _above_shared = ontology.classes_above(shared_dbpedia_class)
        count_from_root = len(_above_shared) - 1  # so root = 0

        return [shared_dbpedia_class, count_from_root,
                count_from_first, count_from_second]


def similar_enough(infobox_first,
                   infobox_second,
                   min_from_root=1,
                   max_from_either_infobox=2):
                   # special_cases = True):
    try:
        _similarity_between = similarity_between(infobox_first, infobox_second)
    except KeyError:
        return False
    else:
        [shared_dbpedia_class, count_from_root,
         count_from_first, count_from_second] = _similarity_between

        # very_general_classes = ['Agent', 'Event', 'Place']
        # _is_special = shared_dbpedia_class in very_general_classes

        # if max_from_either_infobox == 2 and _is_special and special_cases:
        #    max_from_either_infobox = 3

        within_max_from_infobox = (count_from_first <= max_from_either_infobox and
                                   count_from_second <= max_from_either_infobox)

        if within_max_from_infobox and count_from_root >= min_from_root:
            # print _similarity_between, infobox_first, infobox_second
            return True


def post_paraphrase_cleanup(node_list, exclude_unrend, graph=master_graph):
    clean_list = [node for node in node_list if
                  '!!!!!' not in node and 'File:' not in node]
    if exclude_unrend:
        clean_list = [node for node in clean_list if
                      graph.rendering_of_graph_node(node) != 'unrend']

    return clean_list


def _paraphrase_graph(graph, attribute, infoboxes_for_context,
                      intersect, exclude_unrend):

    subgraph = graph.connected_component_with_node(attribute)
    # print "DEBUG: len(subgraph) = " + str(len(subgraph))
    # print {node: graph.infoboxes_of_graph_node(node) for node in subgraph}
    list_of_lists = [[node for node in subgraph if
                      any(similar_enough(infobox, context.lower())
                          for infobox in graph.infoboxes_of_graph_node(node))]
                     for context in infoboxes_for_context]
    if intersect:
        # insersect the list_of_lists
        preliminary_list = list(
            set(list_of_lists[0]).intersection(*list_of_lists))
    else:
        # union the list_of_lists
        preliminary_list = list(set().union(*list_of_lists))

    if attribute in preliminary_list:
        preliminary_list.remove(attribute)

    paraphrases = post_paraphrase_cleanup(preliminary_list, exclude_unrend, graph)

    if len(subgraph) > 10 and len(paraphrases) > 5:
        return []
    else:
        return paraphrases


# As of now, once this function returns paraphrases from Wikipedia
# (through the WikiMap), it does not use WordNet to get more
# paraphrases. In order to do that, the paraphrases will have to first
# run through Loc's infoboxToTexps to be stemmed, lemmatized, etc.
def paraphrase(attribute, infoboxes_for_context,
               intersect=False, exclude_unrend=True):
    """Given an attribute (str) from a Wikipedia infobox and a list of
    infoboxes to use for context-searching, return other attributes
    (and their infobox?) as paraphrases. If attribute does not exist,
    will raise KeyError

    Note on 'intersect' boolean. To be considered: should I do an
    intersection of attributes appropriate for each infobox context,
    or a union? In other words, should more infoboxes_for_context lead
    to less (but more precise) paraphrases, or more (but less
    precise?) paraphrases
    """

    return _paraphrase_graph(master_graph, attribute.lower(),
                             infoboxes_for_context, intersect, exclude_unrend)
