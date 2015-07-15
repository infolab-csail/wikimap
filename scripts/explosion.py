#!/usr/bin/env python2
"""Analyze Explosion

Analyzes the largest indipendant cluster in the graph, showing what
infoboxes appear there, and in what numbers.

Usage: python analyzeExplosion.py [Input Graph File] [Input Excel list
of infobox templates] [Output JSON list of infoboxes]

This program is part of "WikiMap," a system to extract
relationships from Wiki infobox attributes
"""

import sys
import json
import operator
import networkx as nx
from wikimap import data, stats, wikimap
from xlrd import open_workbook


def usage():
    print __doc__


def main(argv):
    try:
        graphInput, listInput, infoboxOutput = argv[0], argv[1], argv[2]
    except IndexError:
        usage()
        sys.exit(2)

    G = data.read_graph(graphInput)
    max_size = max(G.connected_component_lengths())
    max_graph = G.connected_components_with_size(max_size)[0]
    exploded_infoboxes = max_graph.infoboxes_of_graph()

    total_pages = data.total_pages(listInput)

    infobox_totals = data.get_infobox_totals(listInput)
    infobox_pages = {name: total for name, total in infobox_totals.iteritems(
    ) if name in exploded_infoboxes}

    total_missed_pages = sum(infobox_pages.values())

    print 'Done. Writing to disk...'
    data.write_json(infobox_pages, infoboxOutput)

    print
    print 'DONE. Statistics:'

    print stats.fraction_msg(
        "There are",
        total_missed_pages,
        total_pages,
        "Wikipedia pages in the explosion")

    print "In order, missed infoboxes with the most pages:"
    sortedInfoboxes = sorted(infobox_pages.items(), key=operator.itemgetter(1))
    for x in sortedInfoboxes:
        print x

if __name__ == "__main__":
    main(sys.argv[1:])
