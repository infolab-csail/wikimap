#!/usr/bin/env python2

import argparse
import sys

# def status(graph, attribute_mappings):

def main(argv):
    parser = argparse.ArgumentParser(prog='status', description='Show stats about WikiMap')
    parser.add_argument("excel",
                        help="path to input excel of infobox templates")

    parser.add_argument("graph", help="path to output network graph file")
    args = parser.parse_args(argv)

    # print 'Showing graph now.'
    # nx.draw(G,with_labels=True)
    # plt.show()

    print "successfully ran status with {e} and {g}".format(e=args.excel, g=args.graph)


if __name__ == '__main__':
    main(sys.argv[1:])
