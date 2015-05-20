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

    def connected_component_statistics(self):
        """Return a dictionary with the component length and number of such sized components"""
        lengths = self.connected_component_lengths()
        return dict(collections.Counter(lengths))
