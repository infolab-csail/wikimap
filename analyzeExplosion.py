import json
import operator
import networkx as nx
import synonym_network as sn
from xlrd import open_workbook

def percentString(part, total):
    return str(round(100*float(part)/float(total),2)) + '%'

def main():
    G = nx.read_gpickle("data/attributeSynonyms.gpickle")
    maxGraph = G.connected_component_with_size(max(G.connected_component_lengths()))[0]
    explodedInfoboxes = maxGraph.infoboxes_of_graph()
    
    wb = open_workbook('data/infoboxes.xlsx')
    sheet = wb.sheet_by_index(0)

    totalPages = 0
    totalMissedPages = 0
    infoboxPages = {}

    for row in range(2, sheet.nrows):        
        cell = str(sheet.cell(row,0).value)
        numberOfPages = int(sheet.cell(row,1).value) # how many pages
        totalPages += numberOfPages
        infobox = 'Template:Infobox ' + cell.replace('-', ' ')
        # print 'Loading  ' + str(row) + ' of ' + str(sheet.nrows) + " : " + infobox
        if infobox in explodedInfoboxes: 
            infoboxPages[infobox] = numberOfPages
            totalMissedPages += numberOfPages
    
    print 'Done. Writing to disk...'
    with open('data/infoboxesInExplosion.json', 'wb') as fp:
        json.dump(infoboxPages, fp)

    print
    print 'DONE. Statistics:'
    print 'This misses ' + str(int(totalMissedPages)) + ' Wikipedia pages out of ' + str(int(totalPages)) + ' total, or ' + percentString(totalMissedPages, totalPages)
    print 'In order, missed infoboxes with the most pages:'
    sortedInfoboxes = sorted(infoboxPages.items(), key=operator.itemgetter(1))
    for x in sortedInfoboxes: print x

main()
