import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Extracts relationships from Wikipedia infobox attributes.')

    parser.add_argument('command',
                        help="The command to run",
                        choices=[
                            'allinfoboxattributes',
                            'analyzeexplosion',
                            'createnetwork',
                            'findempty',
                            'names',
                            'images',
                        ])

    args = parser.parse_args()
    run_command(args.command)


def run_command(c):
    if c == 'allinfoboxattributes':
        print 'should run allinfoboxattributes'
    elif c == 'analyzeexplosion':
        print 'should analyzeexplosion'
    elif c == 'createnetwork':
        print 'should createnetwork'
    elif c == 'findempty':
        print 'should findempty'
    elif c == 'images':
        print 'should images'


if __name__ == '__main__':
    main()
