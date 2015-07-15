#!/usr/bin/env python2
"""Generate Mappings

Generates mappings between unrendered and rendered wikipedia
attributes, organized by infobox template.

Usage: python generateMappings.py [Input Excel list of infobox
templates] [Output JSON Attribute Mappings]

This program is part of "WikiMap," a system to extract
relationships from Wiki infobox attributes
"""

import sys
import json
import re
from wikipediabase.util import get_infobox, get_meta_infobox
from xlrd import open_workbook


def usage():
    print __doc__


def main(argv):
    try:
        listInput, mappingOutput = argv[0], argv[1]
    except IndexError:
        usage()
        sys.exit(2)

    infoboxAttributes = {}

    wb = open_workbook(listInput)
    sheet = wb.sheet_by_index(0)

    for row in range(2, sheet.nrows):
        # for row in range(2, 10):
        cell = str(sheet.cell(row, 0).value)
        infobox = 'Template:Infobox ' + cell.replace('-', ' ')
        print "Getting {row} of {length} : {infobox}".format(
            row=str(row), length=str(sheet.nrows), infobox=infobox)
        infoboxAttributes[infobox] = get_meta_infobox(infobox).rendered_keys()

    print 'Done. Writing to disk...'
    with open(mappingOutput, 'wb') as fp:
        json.dump(infoboxAttributes, fp)

    print 'DONE.'

if __name__ == "__main__":
    main(sys.argv[1:])
