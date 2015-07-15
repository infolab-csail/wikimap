#!/usr/bin/env python2
"""Find Empty

Finds for what infoboxes we have no attribute mappings, and how many
pages use those 'missed' infoboxes.

Usage: python findEmpty.py [Input JSON Attribute Mappings]
[Input Excel list of infobox templates] [Output JSON list of
infoboxes]

This program is part of "WikiMap," a system to extract
relationships from Wiki infobox attributes
"""

import sys
import json
import operator
from xlrd import open_workbook
from wikimap import data, stats

def usage():
    print __doc__

def main(argv):
    try:
        mappingInput, listInput, infoboxOutput = argv[0], argv[1], argv[2]
    except IndexError:
        usage()
        sys.exit(2)

    mappings = data.get_mappings(mappingInput)
    total_pages = data.total_pages(listInput)

    infobox_totals = data.get_infobox_totals(listInput)
    total_infoboxes = data.total_infoboxes(listInput)
    empty_attributes = {name:total for name,total in infobox_totals.iteritems() if mappings[name] == {}}

    total_missed_pages = sum(empty_attributes.values())
    total_missed_templates = len(empty_attributes)
    most_missed_template = max(empty_attributes.iteritems(), key=operator.itemgetter(1))[0] # key for max value

    print 'Done. Writing to disk...'
    data.write_json(empty_attributes, infoboxOutput)

    print
    print 'DONE. Statistics:'

    print stats.fraction_msg("Missing", total_missed_templates, total_infoboxes, "Infobox templates")

    print stats.fraction_msg("Missing", total_missed_pages, total_pages, "Wikipedia pages")

    print "Missed template with most pages: [{template}] with {number} pages".format(template=most_missed_template, number=str(empty_attributes[most_missed_template]))

if __name__ == "__main__":
    main(sys.argv[1:])
