import json
import networkx as nx
import synonym_network as sn
# import matplotlib.pyplot as plt
# import pydot

def main():
    with open('data/infoboxes.json', 'rb') as fp:
        infoboxAttributes = json.load(fp)
        G=sn.SynonymNetwork()
        numberOfPairs = 0

        for infobox, synonyms in infoboxAttributes.iteritems():
            for unrend, rend in synonyms.iteritems():
                numberOfPairs += 1

                # NODES
                rendState = 'unrend' # first deal with unrend
                for node in (unrend, rend):
                    # To convert into clean strings:
                    # node = str(node.encode('ascii', 'ignore'))
                    
                    if node not in G: G.add_node(node) # if it's not there, add it

                    # whether or not node existed before, it's there now
                    if (infobox in G.node[node].keys()) and (rendState not in G.node[node][infobox]):
                        # if infobox there, but rendState not there already, append rendState
                        G.node[node][infobox].append(rendState)
                    else:       # else (if infobox not there), begin a list with rendState
                        # print 'called'
                        G.node[node][infobox] = [rendState]
                        if len(G.node[node][infobox]) == 2: print G.node[node][infobox]

                    rendState = 'rend' # now we're dealing with rend


                # EDGES
                if not G.has_edge(unrend, rend): G.add_edge(unrend, rend) # if it's not there, add it
                if ('infobox' in G.edge[unrend][rend].keys()) and (infobox not in G.edge[unrend][rend]['infobox']):
                    G.edge[unrend][rend]['infobox'].append(infobox)
                else:
                    G.edge[unrend][rend]['infobox'] = [infobox]
                

        print 'Saving graph...'
        nx.write_gpickle(G,'data/attributeSynonyms.gpickle')
        
        print 'DONE. Graphed a newtork of ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges from ' + str(numberOfPairs) + ' unrendered : rendered attribute pairs, spanning ' + str(len(infoboxAttributes.keys())) + ' infoboxes'

        # print 'Showing graph now.'
        # nx.draw(G,with_labels=True)
        # plt.show()

main()
