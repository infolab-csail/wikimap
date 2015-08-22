#!/usr/bin/env python2
"""Create Network

Creates Network of infobox attributes from saved JSON mappings. To
generate mappings, use generateMappings.py

Usage: python createNetwork.py [Input JSON Attribute Mappings] [Output
File for Graph]

This program is part of "WikiMap," a system to extract
relationships from Wiki infobox attributes
"""

import argparse
import sys
from wikimap import data, stats, graph


def create_graph(infoboxes, clean):
    """Creates and saves a graph to [graph_path] from excel file located at
    [excel_path], optionally [clean]ing (boolean) the graph
    """
    G = graph.WikiMap()

    for infobox in infoboxes:
        for unrend, rend in data.get_single_mappings(infobox).iteritems():
            G.add_mapping(infobox, unrend, rend, clean)

    return G


def main(argv):
    parser = argparse.ArgumentParser(
        prog='create', description='Create a WikiMap')
    parser.add_argument("-c", "--clean",
                        help="make graph with clean nodes",
                        action="store_true")

    parser.add_argument("-s", "--save",
                        help="path to save JSON attribute mappings")

    parser.add_argument("excel",
                        help="path to input excel of infobox templates")

    parser.add_argument("graph", help="path to output network graph file")
    args = parser.parse_args(argv)

    infoboxes = data.get_infoboxes(args.excel)
    G = create_graph(infoboxes, args.clean)

    print("Saving graph...")
    data.write_graph(G, args.graph)

    all_mappings = data.get_all_mappings(args.excel)
    if (args.save):
        data.write_json(all_mappings, args.save)

    print "DONE. Graphed a newtork of {nodes} nodes and {edges} edges " \
        "from {pairs} unrendered : rendered attribute pairs, spanning " \
        "{infoboxes} infoboxes".format(
            nodes=str(G.number_of_nodes()),
            edges=str(G.number_of_edges()),
            pairs=str(stats.dict_sublength(all_mappings)),
            infoboxes=str(data.total_infoboxes(args.excel)))

if __name__ == '__main__':
    main(sys.argv[1:])
