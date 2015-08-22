import argparse
import sys
from wikimap import babble, create, status


def main():
    parser = argparse.ArgumentParser(
        description='Identifies contextual synonyms of Wikipedia Infobox attributes.')

    subparsers = parser.add_subparsers(help='Subcommand to run')

    parser_babble = subparsers.add_parser('babble', help='Print nodenames')
    parser_babble.set_defaults(func=babble.main)

    parser_create = subparsers.add_parser('create', help='Create a WikiMap')
    parser_create.set_defaults(func=create.main)

    parser_status = subparsers.add_parser(
        'status', help='Show stats about WikiMap')
    parser_status.set_defaults(func=status.main)

    args = parser.parse_args(sys.argv[1:2])
    args.func(sys.argv[2:])

if __name__ == '__main__':
    main()
