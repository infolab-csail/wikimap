import json
import re
from wikipediabase.util import get_infobox, get_meta_infobox
from xlrd import open_workbook

def main():
    infoboxAttributes = {}

    wb = open_workbook('infoboxes.xlsx')
    sheet = wb.sheet_by_index(0)

    for row in range(2, sheet.nrows):
    # for row in range(2, 10):
        cell = str(sheet.cell(row,0).value)
        infobox = 'Template:Infobox ' + cell.replace('-', ' ')
        print 'Getting ' + str(row) + ' of ' + str(sheet.nrows) + " : " + infobox
        infoboxAttributes[infobox] = get_meta_infobox(infobox).rendered_keys()
        # for unrend, rend in infoboxAttributes[infobox].iteritems():
        #     print 'unrend : ' + infoboxAttributes[infobox][unrend]
        #     print 'rend : ' + rend
        #     infoboxAttributes[infobox][unrend] = rend.replace(u'\xa0', u' ')
        #     infoboxAttributes[infobox][unrend] = re.sub('\\u[A-Za-z0-9]{4}', ' ', rend) # unicode codes
        #     infoboxAttributes[infobox][unrend] = re.sub('\A\s+', '', rend) # leading whitespace
        #     infoboxAttributes[infobox][unrend] = re.sub('\s+\Z', '', rend) # trailing whitespace
        #     infoboxAttributes[infobox][unrend] = re.sub('\s+', ' ', rend) # repeated whitespace
        
    print 'Done. Writing to disk...'
    with open('infoboxes.json', 'wb') as fp:
        json.dump(infoboxAttributes, fp)

    print 'DONE.'

main()
