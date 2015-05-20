import networkx as nx
import collections

# class SynonymNetwork(nx.DiGraph, nx.Graph):
class SynonymNetwork(nx.DiGraph):
    def __init__(self):
        super(SynonymNetwork, self).__init__()
        self.undirected = super(SynonymNetwork, self).to_undirected() # undirected copy

    def update_undirected(self):
        self.undirected = super(SynonymNetwork, self).to_undirected() # undirected copy

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
