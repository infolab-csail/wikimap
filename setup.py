from setuptools import setup
import multiprocessing

setup(
    name='wikimap',
    version='0.1.0',
    description='Extract relationships from Wiki Infobox Attributes.',
    author='Michael Silver',
    author_email='msilver@csail.mit.edu',
    url='https://github.com/infolab-csail/wikimap.git',
    packages=[
        'wikimap',
        'tests'
    ],
    install_requires=[
        'xlrd',
        'unidecode',
        'nltk',
        'networkx',
        'matplotlib',
        'wikipediabase',
        'defexpand'
    ],
    dependency_links=[
        'git+https://github.com/fakedrake/wikipediabase.git#egg=wikipediabase',
        'git+https://github.com/infolab-csail/defexpand.git#egg=defexpand'
    ],
    tests_require=[
        'nose>=1.0',
        'funcsigs'              # pip forced me to install this
    ],
    entry_points={
        'console_scripts': [
            'wikimap = wikimap.__main__:main',
        ],
    },
    test_suite='nose.collector',
)
