#!/usr/bin/env python2

import networkx as nx
import wikimap
from unidecode import unidecode

def main():
    G = nx.read_gpickle("data/attributeSynonyms.gpickle")
    lengths = G.connected_component_statistics().keys()
    lengths.sort()
    for length in lengths:
        print "length " + str(length) + " node groups:"
        groups = G.connected_components_with_size(length)
        for idx, group in enumerate(groups):
            print "---- number " + str(idx + 1) + " ----"
            for node in group.nodes():
                print unidecode(node)
        print "======================================="

if __name__ == '__main__':
    main()
