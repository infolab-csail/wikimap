# WikiMap
[![Build Status](https://travis-ci.org/infolab-csail/wikimap.svg?branch=master)](https://travis-ci.org/infolab-csail/wikimap)
[![Coverage Status](https://coveralls.io/repos/infolab-csail/wikimap/badge.svg?branch=master&service=github)](https://coveralls.io/github/infolab-csail/wikimap?branch=master)

Identifies contextual synonyms of Wikipedia Infobox attributes by establishing a link between predicate-synonyms and entity classes. Work for the [CSAIL InfoLab](http://groups.csail.mit.edu/infolab/).

Represents synonymy in graphs such as this one:
![Alt text](/../master/images/keyPeople35.png?raw=true "Example Graph")

More detailed results can be seen in the [iPython notebook](/../master/WikiMap%20Analysis.ipynb).

# Install
```Bash 
$ git clone https://github.com/infolab-csail/wikimap.git
$ cd wikimap
wikimap$ python setup.py develop  # to get stay updated on new developments
```
## Note on Graphing
Since `matplotlib` is such a large dependency, but only necessary for graphing networks, it is not included by default. To graph networks, including those in the [iPython notebook](/../master/WikiMap%20Analysis.ipynb), simply install `matplotlib`:
```Bash
$ pip install matplotlib
```

# Paraphrase (Quick Start)
The primary end-product of WikiMap is to paraphrase Wikipedia infobox attributes given some infoboxes as "context" for the paraphrase. You can get this for free simply by **importing WikiMap as a library**:
```Python
>>> from wikimap import synonyms
>>> synonyms.paraphrase("attribute", ["infobox", "other-infobox", ...])
```
Infobox names are case-insensitive, but require dashes instead of spaces. Attribute names have no special requirements, and can have spaces if they so appear on Wikipedia. If the attribute does not exist, `paraphrase()` will throw a `KeyError`. 

`paraphrase()` returns a list of unmodified paraphrases. This means the paraphrases are not stemmed, lemmatized, etc. If no paraphrases are found, pharaphrase will return an empty list.

As of now, the behavior with multiple infoboxes is: paraphrase for each infobox separately, and union all paraphrases. Intersection is possible if you pass `intersect=True` as an optional argument:
```Python
>>> synonyms.paraphrase("attribute", ["infobox", "other-infobox"], intersect=True)
```
By default, unrendered attributes are not given as paraphrases. If you want to see unrendered attributes, pass the `exclude_unrend=False` argument:
```Python
>>> synonyms.paraphrase("attribute", ["infobox", "other-infobox"], exclude_unrend=False)
```
Of course, you can also combine multiple optional arguments together, e.g. 
```Python
>>> synonyms.paraphrase("attribute", ["infobox", "other-infobox"], intersect=True, exclude_unrend=False)
```

## WordNet Synsets
Another useful tool built into WikiMap is the ability to augment the paraphrase data with synonyms from [WordNet](http://wordnetweb.princeton.edu/perl/webwn). To get started, first install the WordNet corpus:
```Bash
$ python2.7 -c "import nltk; nltk.download('wordnet');"
```
To get synonyms from WordNet, WikiMap comes with the `id_synset()` function. Normally, WordNet has many synsets for each word, each for a different usage of the word. To overcome this problem, `id_synset()` allows you to give "example" synonyms (one or more) for a word, and `id_synset()` will return a list similar synonyms. Here are some examples:
```Python
>>> from wikimap import synonyms
>>> synonyms.id_synset('dog', ['canis familiaris'])
['dog', 'domestic dog', 'canis familiaris']

>>> synonyms.id_synset('dog', ['wiener'])
['frank', 'frankfurter', 'hotdog', 'hot dog', 'dog', 'wiener', 'wienerwurst', 'weenie']

>>> synonyms.id_synset('maintain', ['sustain'])
['sustain', 'keep', 'maintain']

>>> synonyms.id_synset('maintain', ['assert'])
['assert', 'asseverate', 'maintain']

>>> synonyms.id_synset('maintain', ['conserve'])
['conserve', 'preserve', 'maintain', 'keep up']
```
Or in general:
```Python
>>> synonyms.id_synset('word', ['example', 'example2', ...])
```

All words, including examples, provided to `id_synset()` must be stemmed, lemmatized, singular, etc.

Attempting to find synonyms for a word that is not in WordNet will result in a `KeyError`. If there are either no synsets for a given word that match the given "example" synonyms, or if the "example" synonyms are insufficient to id one synset, then a `RuntimeError` is raised (although different messages are provided for debugging purposes). Ex:
```Python
>>> synonyms.id_synset('asdf', ['junk'])
KeyError: 'WordNet contains no synsets for word: asdf'

>>> synonyms.id_synset('dog', ['junk'])
RuntimeError: No synset of <dog> matches keys

>>> synonyms.id_synset('maintain', ['keep'])
RuntimeError: Keys insufficient to uniquely identify synset, 5 synsets found

>>> synonyms.id_synset('maintain', ['keep', 'hold'])
['keep', 'maintain', 'hold']
```

# Other Usage
While WikiMap comes with a pre-compiled WikiMap graph already, it also comes with the souce needed to **make a new WikiMap graph**. The install gives you one Command Line Interface entrypoint called `wikimap`. All commands are run as subcommands of `wikimap`. You can run any subcommand by running:
```Bash
$ wikimap <SUBCOMMAND> <OPTIONS>
```
For up-to-date documentation and a list of all subcommands, simply run
```Bash
$ wikimap -h
```

For up-to-date documentation on any of the listed subcommands, simply run
```Bash
$ wikimap <SUBCOMMAND> -h
```

Major subcommands:
## `create`
`wikimap create <OPTIONS>` creates a new WikiMap graph, which represents relationships between infobox attributes. An example graph can be seen at the top of the README. 

## `status`
`wikimap status <OPTIONS>` prints statistics and information about an existant graph.

## `babble`
`wikimap babble <OPTIONS>` prints all of the nodes in a graph. This command is commonly used in conjunction with a redirect into a file, e.g. `wikimap babble <OPTIONS> > my-output-file.txt`
