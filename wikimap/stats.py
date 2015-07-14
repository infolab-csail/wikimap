import networkx as nx
import wikimap

def percent_str(part, total):
    return str(round(100*float(part)/float(total),2)) + '%'
