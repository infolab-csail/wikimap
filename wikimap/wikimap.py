import networkx as nx
import collections


class WikiMap(nx.DiGraph):
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
        """Return a list of connected component of a given size"""
        components = [x for x in nx.connected_component_subgraphs(
            self.return_undirected()) if x.number_of_nodes() == size]
        for graph in components:
            WikiMap.convert_to_special(graph)

        return components

    # SPECIFIC WIKI INFOBOX/ATTRIBUTE METHODS:
    def infoboxes_of_graph_node(self, nodeName):
        """Return a list of infoboxes of a node"""
        return self.node[nodeName].keys()

    def infoboxes_of_graph(self):
        """Return a (non-redunant) list of a graph's infoboxes"""
        infoboxes = []
        for nodeName in super(WikiMap, self).nodes():
            infoboxes = infoboxes + self.infoboxes_of_graph_node(nodeName)
        return list(set(infoboxes))

    def rendering_of_graph_node(self, nodeName):
        """Return either 'unrend', 'rend', or 'mixed' about a node"""
        rendingList = [item for sublist in self.node[nodeName].values(
        ) for item in sublist]
        # due to flattening [['unrend'],['rend','unrend']] etc.

        if all(items == 'unrend' for items in rendingList):
            return 'unrend'
        elif all(items == 'rend' for items in rendingList):
            return 'rend'
        else:
            return 'mixed'

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
