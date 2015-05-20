import networkx as nx
import collections

class SynonymNetwork(nx.DiGraph):
    # CLASS MAINTENENCE:
    def __init__(self):
        super(SynonymNetwork, self).__init__()
        self.undirected = super(SynonymNetwork, self).to_undirected() # undirected copy

    def update_undirected(self):
        self.undirected = super(SynonymNetwork, self).to_undirected() # undirected copy

    @classmethod
    def convert_to_special(cls, obj):
        obj.__class__ = SynonymNetwork
        obj.update_undirected()

    # GENERAL NETWORK METHODS:
    def connected_component_lengths(self):
        """Return a list of the lengths of each component"""
        self.update_undirected()
        return [len(x) for x in nx.connected_components(self.undirected)]

    def connected_component_statistics(self, printStats=False):
        """Return a dictionary with the component length and number of such sized components"""
        lengths = self.connected_component_lengths()
        lengthDict = dict(collections.Counter(lengths))

        if printStats:
            orderedLengthDict = collections.OrderedDict(sorted(lengthDict.items()))
            numberOfGroups = nx.number_connected_components(self.undirected)
            for k, v in orderedLengthDict.iteritems():
                percent = round((100.00*v / numberOfGroups), 2)
                print str(k) + ' nodes: ' + str(v) + ' (' + str(percent) + '%) groups'
            print '-----------------------------------------'
            print 'TOTAL: ' + str(super(SynonymNetwork, self).number_of_nodes()) + ' nodes in network, ' + str(numberOfGroups) + ' distinct groups'
        
        return lengthDict

    def connected_component_with_size(self, size):
        """Return a list of connected component of a given size"""
        components = [x for x in nx.connected_component_subgraphs(self.undirected) if x.number_of_nodes() == size]
        for graph in components:
            SynonymNetwork.convert_to_special(graph)

        return components

    
    # SPECIFIC WIKI INFOBOX/ATTRIBUTE METHODS:
    def infoboxes_of_graph_node(self, nodeName):
        """Return a list of infoboxes of a node"""
        return self.node[nodeName].keys()

    def infoboxes_of_graph(self):
        """Return a (non-redunant) list of a graph's infoboxes"""
        infoboxes = []
        for nodeName in self.nodes():
            infoboxes = infoboxes + self.infoboxes_of_graph_node(nodeName)
        return list(set(infoboxes))
