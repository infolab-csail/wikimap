# Senior Thesis
Code &amp; docs related to my BU Academy senior thesis work at the [CSAIL InfoLab](http://groups.csail.mit.edu/infolab/)

## Files
File   	 | Description
-------- | -----------
`allInfoboxAttributes.py` |  Loops through `infoboxes.xlsx` and creates a JSON dictionary (`infoboxes.json`) with all of the   `unrendered : rendered` attribute pairs, organized by infobox template name
`findEmpty.py`  | Saves another JSON file with a list of `{"Template:Infobox <missed infobox1>" : # of pages, "Template:Infobox <missed infobox2>" : # of pages, … etc}` for infoboxes that `get_meta_infobox('<TEMPLATE_NAME>').rendered_keys()` returns `{}`
`createNetwork.py` | Creates a network of unrendered and rendered infobox attributes in an attempt to identify synonyms. Each node is an attribute, and a directed edge links an unrendered to rendered attribute (in that direction).

