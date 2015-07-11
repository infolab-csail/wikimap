from setuptools import setup

setup(
    name='Attribute-Analyzer',
    version='1.0',
    description='Extract relationships from Wiki Infobox Attributes.',
    author='Michael Silver',
    author_email='msilver@csail.mit.edu',
    url='https://github.com/michaelsilver/Attribute-Analyzer',
    packages=['attribute_analyzer'],
    install_requires=[
        'xlrd',
        'networkx',
        'wikipediabase'
    ],
    dependency_links=[
        # The upstream version on pypi will probably be out of date
        # until this gets deployed
        'git+https://github.com/fakedrake/wikipediabase.git#egg=wikipediabase'
    ],
    entry_points={
        'console_scripts': [
            'allinfoboxattributes = attribute_analyzer.allInfoboxAttributes:main',
            'analyzeexplosion = attribute_analyzer.analyzeExplosion:main',
            'createnetwok = attribute_analyzer.createNetwork:main',
            'findempty = attribute_analyzer.findEmpty:main',
            'names = attribute_analyzer.names:main',
            'images = attribute_analyzer.images:main',
        ],
    },

)
