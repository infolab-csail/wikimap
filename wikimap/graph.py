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
import json
from unidecode import unidecode
import re
import string
import networkx as nx
import wikimap

badPunct = list(string.punctuation)
badPunct.remove('_')            # will be dealt with separately (replaced with space)
badPunct.remove('-')            # will be dealt with separately (replaced with space)
badPunct.remove("'")            # will be dealt with separately (checking for 's)
badPunct.remove('%')            # "% of total exports"
badPunct.remove(',')            # "Managing editor, design"
badPunct.remove('$')            # "MSRP US$"
badPunct.remove('&')            # "Specific traits & abilities"

html = re.compile("<.*?>")
brackets = re.compile("\[.*?\]")
parens = re.compile("\(.*?\)")
noPossesive = re.compile("(?<!s)'(?!s)")

def clean(node):
    node = unidecode(node)      # transliterate unicode

    # leave the special '!!!!!' and 'File:' nodes alone, will be used as "bridges"
    if '!!!!!' not in node and 'File:' not in node:
        # strip all html, brackets, parens
        node = re.sub(html, '', node)
        node = re.sub(brackets, '', node)
        node = re.sub(parens, '', node)
        node = node.replace('&mdot;', '')

        # check for possessive ('s or s' or s's); if none, strip all '
        node = re.sub(noPossesive, '', node)

        # replace all dashes and underscores with a space
        node = node.replace('_', ' ')
        node = node.replace('-', ' ')

        # strip all remaining punctuation
        for punct in badPunct:
            node = node.replace(punct, '')

        node = node.lower()           # lowercase
        node = ' '.join(node.split()) # replace all multiple spaces with one
    return node

def addToField(location, field, value):
    if (field in location.keys()) and (value not in location[field]):
        location[field].append(value)
    else:
        location[field] = [value]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clean", help="make graph with clean nodes",
                    action="store_true")
    parser.add_argument("mappings", help="path to input JSON list of infoboxes")
    parser.add_argument("graph", help="path to output network graph file")
    # TODO:
    #   - add function to clean nodes when -c is passed
    #   - work on cleaning function
    args = parser.parse_args()

    with open(args.mappings, 'rb') as fp:
        infoboxAttributes = json.load(fp)
        G=wikimap.WikiMap()
        numberOfPairs = 0

        for infobox, synonyms in infoboxAttributes.iteritems():
            for unrend, rend in synonyms.iteritems():
                numberOfPairs += 1

                if args.clean:
                    cleanVersion = {node:clean(node) for node in (unrend, rend)}
                    for node in (unrend, rend):
                        G.add_node(cleanVersion[node])
                        addToField(G.node[cleanVersion[node]], 'was', node)
                    unrend = cleanVersion[unrend]
                    rend = cleanVersion[rend]

                G.add_edge(unrend, rend)

                # NODE ATTRIBUTES
                rendState = 'unrend' # first deal with unrend
                for node in (unrend, rend):
                    addToField(G.node[node], infobox, rendState)
                    rendState = 'rend' # now we're dealing with rend

                # EDGE ATTRIBUTES
                addToField(G.edge[unrend][rend], 'infobox', infobox)

        print 'Saving graph...'
        nx.write_gpickle(G, args.graph)
        
        print 'DONE. Graphed a newtork of ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges from ' + str(numberOfPairs) + ' unrendered : rendered attribute pairs, spanning ' + str(len(infoboxAttributes.keys())) + ' infoboxes'

        # print 'Showing graph now.'
        # nx.draw(G,with_labels=True)
        # plt.show()

if __name__ == '__main__':
    main()
