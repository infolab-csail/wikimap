# WikiMap
Extract useful relationships from Wikipedia's Infobox attributes using mappings from Chris's [WikipediaBase](https://github.com/fakedrake/WikipediaBase). Work for the [CSAIL InfoLab](http://groups.csail.mit.edu/infolab/)

_previously known as "Attribute Analyzer"_

## Generating an Infobox Attribute Graph
How to extract unrendered ==> rendered mappings from Chris's WikipediaBase, and then create a network (or graph) such as this one:
![Alt text](/../master/images/keyPeople35.png?raw=true "Example Graph")

Steps:

1: First, find a machine with Chris's [WikipediaBase](https://github.com/fakedrake/WikipediaBase) installed, or otherwise install WikipediaBase.
```Bash
$ git clone https://github.com/fakedrake/WikipediaBase.git
$ sudo pip install wikipediabase
$ sudo apt-get install libxml2-dev libxslt1-dev python-dev  # some ubuntu machines might not have some packages installed
$ sudo pip install -r requirements.txt
```

2: Clone this repo and copy some key files onto the machine with WikipediaBase installed.
```Bash
$ git clone https://github.com/michaelsilver/Attribute-Analyzer.git
$ cp Attribute-Analyzer/createNetwork.py WikipediaBase/
$ cp Attribute-Analyzer/synonym_network.py WikipediaBase/
```
You will also need to put `infoboxes.xlsx` in the `WikipediaBase` directory. If you have it on your computer, you can use `scp`. Syntax: `scp /path/to/file username@a:/path/to/destination`

3: Run `allInfoboxAttributes.py` and `infoboxes.json` should pop up.
```
$ python allInfoboxAttributes.py
```
Congratulations, you've now stolen all the data out of WikipediaBase that we need! All the unrendered ==> rendered attribute mappings are now stored in `infoboxes.json`

4: Put a full clone of the repo on any machine of your choosing, and put `infoboxes.json`. This way you will be indipendant of WikipediaBase
```Bash
$ git clone https://github.com/michaelsilver/Attribute-Analyzer.git
$ mkdir data/  # to structure the repo the way we need it
$ scp username@remote-machine:/path/to/file ./data/  # put infoboxes.json where it needs to be
$ python createNetwork.py
```
Now the graph is saved in `data/attributeSynonyms.gpickle`. All done; you now have the graph, proceed to "Analyzing the Attribute Graph"

## Analyzing the Attribute Graph
All analysis tools are located in the `synonym_network.py` libarary. To use it, import the necessary libaries, load the saved graph, and you can then do whatever analysis you want.
```Bash
$ python
>>> import networkx as nx
>>> import synonym_network as sn
>>> G = nx.read_gpickle("data/attributeSynonyms.gpickle")
```
Then you can do whatever you want with the graph now saved in the variable `G`; for example,
```Python
>>> G.nodes()
```
will print out all the nodes in the network.
