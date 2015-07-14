import argparse

usage = '''wikimap <command>

Commands:
    attributes     Get all infobox attributes
    create         Create network
    explosion      Analyze the explosion
    findempty      Find empty
    images         Get images
    names          Get names
'''


def main():
    parser = argparse.ArgumentParser(
        description='Extracts relationships from Wikipedia infobox attributes.',
        usage=usage)

    parser.add_argument('<command>',
                        help='Subcommand to run',
                        choices=[
                            'attributes',
                            'create',
                            'explosion',
                            'findempty',
                            'images',
                            'names',
                        ])

    args = parser.parse_args()
    run_command(args.command)


def run_command(c):
    # TODO : call wikimap methods
    if c == 'attributes':
        print 'wikimap called with command: attributes'
    elif c == 'create':
        print 'wikimap called with command: create'
    elif c == 'explosion':
        print 'wikimap called with command: explosion'
    elif c == 'findempty':
        print 'wikimap called with command: findempty'
    elif c == 'images':
        print 'wikimap called with command: images'
    elif c == 'names':
        print 'wikimap called with command: names'


if __name__ == '__main__':
    main()
