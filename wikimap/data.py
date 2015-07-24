import itertools
import json
from xlrd import open_workbook
import networkx as nx


# READING

# add caching decorator
def read_json(path):
    with open(path, 'rb') as fp:
        return json.load(fp)


def read_graph(path):
    return nx.read_gpickle(path)


# add caching decorator
def get_infobox_totals(path):
    """Returns a dictionary where keys are infobox templates (str) and
    values (float) are how many pages use the template. Infobox name
    of form 'Template:Infobox foo bar'.
    """
    wb = open_workbook(path)
    sheet = wb.sheet_by_index(0)

    # get the names
    names = sheet.col_values(0, 2)  # 0th col, starting at 2nd row

    # makes a template name formal according to wikipedia
    formal_name = lambda cell: 'Template:Infobox ' + str(cell).replace('-', ' ')

    # if an integer float turn into integer; else leave it alone
    int_integer = lambda name: int(name) if isinstance(name, float) and name.is_integer() else name

    formal_names = [formal_name(int_integer(cell)) for cell in names]

    # get the number of pages for each name
    numbers = sheet.col_values(1, 2)  # 1th col, starting at 2nd row

    # return a dictionary of form {name: number of pages}
    return dict(itertools.izip(formal_names, numbers))


# get_infoboxes()
def _get_infoboxes(infobox_totals):
    return infobox_totals.keys()


# TODO: add caching decorator
def get_infoboxes(path):
    _get_infoboxes(get_infobox_totals(path))


# total_infoboxes()
def _total_infoboxes(infobox_totals):
    return len(infobox_totals)


# TODO: add caching decorator
def total_infoboxes(path):
    _total_infoboxes(get_infobox_totals(path))


# total_pages()
def _total_pages(infobox_totals):
    return sum(infobox_totals.values())


# TODO: add caching decorator
def total_pages(path):
    _total_pages(get_infobox_totals(path))


# WRITING

def write_json(dict, path):
    with open(path, 'wb') as fp:
        json.dump(dict, fp)
