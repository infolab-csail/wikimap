#!/usr/bin/env python2
"""Create Network

Creates Network of infobox attributes from saved JSON mappings. To
generate mappings, use generateMappings.py

Usage: python createNetwork.py [Input JSON Attribute Mappings] [Output
File for Graph]

This program is part of "Attribute Analyzer," a system to extract
relationships from Wiki infobox attributes
"""

import sys
import json
import networkx as nx
import synonym_network as sn
# import matplotlib.pyplot as plt
# import pydot

def usage():
    print __doc__

def main(argv):
    try:
        mappingInput, graphOutput = argv[0], argv[1]
    except IndexError:
        usage()
        sys.exit(2)

    with open(mappingInput, 'rb') as fp:
        infoboxAttributes = json.load(fp)
        G=sn.SynonymNetwork()
        numberOfPairs = 0

        for infobox, synonyms in infoboxAttributes.iteritems():
            for unrend, rend in synonyms.iteritems():
                numberOfPairs += 1

                G.add_edge(unrend, rend)
                # To convert into clean strings:
                # node = str(node.encode('ascii', 'ignore'))

                # NODE ATTRIBUTES
                rendState = 'unrend' # first deal with unrend
                for node in (unrend, rend):

                    if (infobox in G.node[node].keys()) and (rendState not in G.node[node][infobox]):
                        # if infobox there, but rendState not there already, append rendState
                        G.node[node][infobox].append(rendState)
                    else:       # else (if infobox not there), begin a list with rendState
                        # print 'called'
                        G.node[node][infobox] = [rendState]
                        if len(G.node[node][infobox]) == 2: print G.node[node][infobox]

                    rendState = 'rend' # now we're dealing with rend


                # EDGE ATTRIBUTES
                if ('infobox' in G.edge[unrend][rend].keys()) and (infobox not in G.edge[unrend][rend]['infobox']):
                    G.edge[unrend][rend]['infobox'].append(infobox)
                else:
                    G.edge[unrend][rend]['infobox'] = [infobox]
                

        print 'Saving graph...'
        nx.write_gpickle(G, graphOutput)
        
        print 'DONE. Graphed a newtork of ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges from ' + str(numberOfPairs) + ' unrendered : rendered attribute pairs, spanning ' + str(len(infoboxAttributes.keys())) + ' infoboxes'

        # print 'Showing graph now.'
        # nx.draw(G,with_labels=True)
        # plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
