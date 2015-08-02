#!/usr/bin/env python2

import argparse
import sys
from unidecode import unidecode
from wikimap import data, graph


def main(argv):
    parser = argparse.ArgumentParser(prog='babble',
                                     description='Print nodenames')
    parser.add_argument("graph", help="path to input networkx graph file")
    args = parser.parse_args(argv)

    G = data.read_graph(args.graph)
    graph.WikiMap.convert_to_special(G)
    lengths = sorted(G.connected_component_statistics().keys())
    for length in lengths:
        print "length " + str(length) + " node groups:"
        groups = G.connected_components_with_size(length)
        for idx, group in enumerate(groups):
            print "---- number " + str(idx + 1) + " ----"
            for node in group.nodes():
                print unidecode(node)
        print "======================================="

if __name__ == '__main__':
    main(sys.argv[1:])
