import networkx as nx
import collections
from unidecode import unidecode
import re
import string


class WikiMap(nx.DiGraph):

    bad_punct = list(string.punctuation)
    # will be dealt with separately (replaced with space)
    bad_punct.remove('_')
    # will be dealt with separately (replaced with space) -- actually
    # experimenting with leaving the dash there
    bad_punct.remove('-')
    # will be dealt with separately (checking for 's)
    bad_punct.remove("'")
    bad_punct.remove('%')            # "% of total exports"
    bad_punct.remove(',')            # "Managing editor, design"
    bad_punct.remove('$')            # "MSRP US$"
    bad_punct.remove('&')            # "Specific traits & abilities"

    html = re.compile("<.*?>")
    brackets = re.compile("\[.*?\]")
    parens = re.compile("\(.*?\)")
    no_possesive = re.compile("(?<!s)'(?!s)")

    # CLASS MAINTENENCE:

    def __init__(self):
        super(WikiMap, self).__init__()
        self.__undirectedCopy = super(
            WikiMap, self).to_undirected()  # undirected copy

    def update_undirected(self):
        self.__undirectedCopy = super(
            WikiMap, self).to_undirected()  # undirected copy

    def return_undirected(self):
        self.update_undirected()
        return self.__undirectedCopy

    @classmethod
    def convert_to_special(cls, obj):
        obj.__class__ = WikiMap
        obj.update_undirected()

    # GENERAL NETWORK METHODS:
    def connected_component_lengths(self):
        """Return a list of the lengths of each component"""
        return [len(x)
                for x in nx.connected_components(self.return_undirected())]

    def connected_component_statistics(self, printStats=False):
        """Return a dictionary with the component length and number of
        such sized components
        """
        lengths = self.connected_component_lengths()
        lengthDict = dict(collections.Counter(lengths))

        if printStats:
            orderedLengthDict = collections.OrderedDict(
                sorted(lengthDict.items()))
            numberOfGroups = nx.number_connected_components(
                self.return_undirected())
            for k, v in orderedLengthDict.iteritems():
                percent = round((100.00 * v / numberOfGroups), 2)
                print "{k} nodes: {v} ({percent}%) groups".format(
                    k=k, v=v, percent=str(percent))
            print '-----------------------------------------'
            print "TOTAL: {t} nodes in network, {g} distinct groups".format(
                t=str(super(WikiMap, self).number_of_nodes()),
                g=str(numberOfGroups))
        else:
            return lengthDict

    def connected_components_with_size(self, size):
        """Return a list of connected component of a given size
        WARNING: directionality of graph lost in process
        """
        components = [x for x in nx.connected_component_subgraphs(
            self.return_undirected()) if x.number_of_nodes() == size]
        for graph in components:
            WikiMap.convert_to_special(graph)

        return components

    # SPECIFIC WIKI INFOBOX/ATTRIBUTE METHODS:

    # FETCHING INFORMATION
    def infoboxes_of_graph_node(self, nodeName):
        """Return a list of infoboxes of a node"""
        return self.node[nodeName]['infobox'].keys()

    def infoboxes_of_graph(self):
        """Return a (non-redunant) list of a graph's infoboxes"""
        infoboxes = []
        for node_name in super(WikiMap, self).nodes():
            infoboxes = infoboxes + self.infoboxes_of_graph_node(node_name)
        return list(set(infoboxes))

    def rendering_of_graph_node(self, nodeName):
        """Return either 'unrend', 'rend', or 'mixed' about a node"""
        rendingList = [item for sublist in self.node[nodeName]['infobox'].values(
        ) for item in sublist]
        # due to flattening [['unrend'],['rend','unrend']] etc.

        if all(items == 'unrend' for items in rendingList):
            return 'unrend'
        elif all(items == 'rend' for items in rendingList):
            return 'rend'
        else:
            return 'mixed'

    def infoboxes_of_pair(self, unrend, rend):
        return self.edge[unrend][rend]['infobox']

    # INSERTING INFORMATION
    @staticmethod
    def clean(node):
        if isinstance(node, unicode):
            node = unidecode(node)      # transliterate unicode

        # leave the special '!!!!!' and 'File:' nodes alone, will be used as
        # "bridges"
        if '!!!!!' not in node and 'File:' not in node:
            # strip all html, brackets, parens
            node = re.sub(WikiMap.html, '', node)
            node = re.sub(WikiMap.brackets, '', node)
            node = re.sub(WikiMap.parens, '', node)
            node = node.replace('&mdot;', '')

            # check for possessive ('s or s' or s's); if none, strip all '
            node = re.sub(WikiMap.no_possesive, '', node)

            # replace all dashes and underscores with a space
            node = node.replace('_', ' ')
            # node = node.replace('-', ' ')

            # strip all remaining punctuation
            for punct in WikiMap.bad_punct:
                node = node.replace(punct, '')

            node = node.lower()           # lowercase
            # replace all multiple spaces with one
            node = ' '.join(node.split())
        return node

    @staticmethod
    def add_to_field(location, field, value):
        if (field in location.keys()) and (value not in location[field]):
            location[field].append(value)
        else:
            location[field] = [value]

    def add_uncleaned(self, unrend, rend):
        for node in (unrend, rend):
            clean_node = WikiMap.clean(node)
            self.add_node(clean_node)
            WikiMap.add_to_field(self.node[clean_node], 'was', node)

    def _add_node_rendering(self, infobox, node, rend_state):
        if 'infobox' not in self.node[node].keys():
            self.node[node]['infobox'] = {}
        WikiMap.add_to_field(
            self.node[node]['infobox'], infobox, rend_state)

    def add_rendering(self, infobox, unrend, rend):
        rend_state = 'unrend'  # first deal with unrend
        for node in (unrend, rend):
            self._add_node_rendering(infobox, node, rend_state)
            rend_state = 'rend'  # now we're dealing with rend

    def add_infobox(self, infobox, unrend, rend):
        WikiMap.add_to_field(self.edge[unrend][rend], 'infobox', infobox)

    def add_mapping(self, infobox, unrend, rend, clean):
        """Add mapping for [infobox] (str) between [unrendered] (str) and
        [rendered] (str) to the specified [graph] (WikiMap object)"""
        if WikiMap.clean:
            self.add_uncleaned(unrend, rend)
            unrend = WikiMap.clean(unrend)
            rend = WikiMap.clean(rend)

        self.add_edge(unrend, rend)

        self.add_rendering(infobox, unrend, rend)
        self.add_infobox(infobox, unrend, rend)

    # ANALYTICS:
    def connected_component_nodes_with_size(
            self, size, showRending=False, printResults=False):
        """Return a list of nodes for each connected component of a
        given size, optionally showing the rendering state ('rend',
        'unrend', or 'mixed'), and optionally priting the results in a
        readable manner"""

        graphsOfSize = self.connected_components_with_size(size)
        if showRending:
            ans = [{node: graph.rendering_of_graph_node(node) for node in super(
                WikiMap, graph).nodes()} for graph in graphsOfSize]
        else:
            ans = [super(WikiMap, graph).nodes() for graph in graphsOfSize]

        if printResults:
            for x in ans:
                if showRending:
                    for k, v in x.iteritems():
                        print k + ' (' + v + ')'
                    print
                else:
                    print x
        else:
            return ans
