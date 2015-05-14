# Senior Thesis
All code &amp; docs related to my BU Academy senior thesis work at the CSAIL InfoLab

## Files
File   	 | Description
-------- | -----------
`allInfoboxAttributes.py` |  Loops through `infoboxes.xlsx` and creates a JSON dictionary (`infoboxes.json`) with all of the   `unrendered : rendered` attribute pairs, organized by infobox template name
`findEmpty.py`  | Saves another JSON file with a list of `{"Template:Infobox <missed infobox1>" : # of pages, "Template:Infobox <missed infobox2>" : # of pages, … etc}` for infoboxes that `get_meta_infobox('<TEMPLATE_NAME>').rendered_keys()` returns `{}`

