#!/usr/bin/env python2

import argparse
import sys
import networkx as nx
import matplotlib.pyplot as plt
from wikimap import data, graph


def main(argv):
    parser = argparse.ArgumentParser(prog='capture',
                                     description='Capture images of subgraphs')
    parser.add_argument("graph", help="path to input networkx graph file")
    parser.add_argument("images", help="path to output directory for images")
    args = parser.parse_args(argv)

    G = data.read_graph(args.graph)
    lengths = G.connected_component_statistics().keys()
    lengths.sort(reverse=True)
    for len in lengths:
        print "length " + str(len) + " node groups:"
        subGraphs = G.connected_components_with_size(len)
        for idx, sub in enumerate(subGraphs):
            print "---- number " + str(idx + 1) + " ----"
            nx.draw(sub, with_labels=True, arrows=True)
            plt.savefig(args.images + "len-" + str(len) +
                        "-num-" + str(idx + 1) + ".png", bbox_inches="tight")
        print "======================================="

if __name__ == '__main__':
    main(sys.argv[1:])
