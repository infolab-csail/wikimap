from setuptools import setup

setup(
    name='wikimap',
    version='0.1.0',
    description='Extract relationships from Wiki Infobox Attributes.',
    author='Michael Silver',
    author_email='msilver@csail.mit.edu',
    url='https://github.com/michaelsilver/wikimap',
    packages=['wikimap'],
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
            'wikimap = wikimap.__main__:main',
        ],
    },

)
