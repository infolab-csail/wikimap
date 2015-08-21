#!/usr/bin/env python2

import argparse
import sys
import operator
from wikimap import data, stats, graph


def find_empty(excel, empty_report):
    mappings = data.get_all_mappings(excel)
    total_pages = data.total_pages(excel)

    infobox_totals = data.get_infobox_totals(excel)
    total_infoboxes = data.total_infoboxes(excel)
    empty_attributes = {
        name: total for name,
        total in infobox_totals.iteritems() if mappings[name] == {}}

    total_missed_pages = sum(empty_attributes.values())
    total_missed_templates = len(empty_attributes)
    most_missed_template = max(
        empty_attributes.iteritems(),
        key=operator.itemgetter(1))[0]  # key for max value

    print 'Done. Writing to disk...'
    data.write_json(empty_attributes, empty_report)

    print
    print 'DONE. Statistics:'

    print stats.fraction_msg(
        "Missing",
        total_missed_templates,
        total_infoboxes,
        "Infobox templates")

    print stats.fraction_msg(
        "Missing",
        total_missed_pages,
        total_pages,
        "Wikipedia pages")

    print "Missed template with most pages: [{template}] with {number} " \
        "pages".format(template=most_missed_template, number=str(int(
            empty_attributes[most_missed_template])))


def analyze_explosion(G, excel, explosion_report):
    max_size = max(G.connected_component_lengths())
    max_graph = G.connected_components_with_size(max_size)[0]
    exploded_infoboxes = max_graph.infoboxes_of_graph()

    total_pages = data.total_pages(excel)

    infobox_totals = data.get_infobox_totals(excel)
    infobox_pages = {name: total for name, total in infobox_totals.iteritems(
    ) if name in exploded_infoboxes}

    total_missed_pages = sum(infobox_pages.values())

    print 'Done. Writing to disk...'
    data.write_json(infobox_pages, explosion_report)

    print
    print 'DONE. Statistics:'

    print stats.fraction_msg(
        "There are",
        total_missed_pages,
        total_pages,
        "Wikipedia pages in the explosion")

    print "In order, missed infoboxes with the most pages:"
    sortedInfoboxes = sorted(infobox_pages.items(), key=operator.itemgetter(1),
                             reverse=True)
    for x in sortedInfoboxes:
        print x


def status(graph, explosion_report, excel, empty_report):
    G = data.read_graph(graph)

    print "CONNECTED COMPONENTS..."
    G.connected_component_statistics(printStats=True)

    print "======================================="
    print "FINDING EMPTY..."
    find_empty(excel, empty_report)

    print "======================================="
    print "ANALYZING EXPLOSION..."
    analyze_explosion(G, excel, explosion_report)


def main(argv):
    parser = argparse.ArgumentParser(
        prog='status', description='Show stats about WikiMap')
    parser.add_argument("graph", help="path to input network graph file")
    parser.add_argument("excel",
                        help="path to input excel of infobox templates")
    parser.add_argument("empty_report",
                        help="path to JSON output file for empty report")
    parser.add_argument("explosion_report",
                        help="path to JSON output file for explosion report")
    args = parser.parse_args(argv)
    status(args.graph, args.explosion_report, args.excel, args.empty_report)


if __name__ == '__main__':
    main(sys.argv[1:])
