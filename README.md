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

# Usage
The install gives you one Command Line Interface entrypoint called `wikimap`. All commands are run as subcommands of `wikimap`. You can run any subcommand by running:
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
