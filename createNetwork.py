import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
    with open('data/infoboxes.json', 'rb') as fp:
        infoboxAttributes = json.load(fp)
        G=nx.DiGraph()
        numberOfPairs = 0

        for infobox, synonyms in infoboxAttributes.iteritems():
            for unrend, rend in synonyms.iteritems():
                numberOfPairs += 1
                G.add_edge(unrend, rend)

        print 'Saving graph...'
        nx.write_gpickle(G, 'data/attributeSynonyms.gpickle')
        
        print 'DONE. Graphed a newtork of ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges from ' + str(numberOfPairs) + ' unrendered : rendered attribute pairs, spanning ' + str(len(infoboxAttributes.keys())) + ' infoboxes'

        print 'Showing graph now.'
        nx.draw_circular(G,with_labels=True)
        plt.show()

main()
