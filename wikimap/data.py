import itertools
import json
from xlrd import open_workbook
import networkx as nx
from wikipediabase.infobox import get_meta_infobox


# READING

# add caching decorator
def read_json(path):
    """Given path to a json file, return json as python dict"""
    with open(path, 'rb') as fp:
        return json.load(fp)


def read_graph(path):
    """Given path to gpickle, return a networkx graph object"""
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

    # if an integer float turn into integer; else leave it alone
    int_integer = lambda name: int(name) if isinstance(
        name, float) and name.is_integer() else name

    other_names = [str(int_integer(cell)) for cell in names]

    # get the number of pages for each name
    numbers = sheet.col_values(1, 2)  # 1th col, starting at 2nd row

    # return a dictionary of form {name: number of pages}
    return dict(itertools.izip(other_names, numbers))


def get_formal_name(infobox):
    return 'Template:Infobox ' + infobox.replace('-', ' ')


def get_single_mappings(infobox):
    """Given one infobox, return its attribute mappings"""
    return get_meta_infobox(get_formal_name(infobox)).attributes


def get_all_mappings(path):
    """Given path to excel file, return dictionary with attribute mappings"""
    return _get_all_mappings(get_infoboxes(path))


def _get_all_mappings(infoboxes):
    """Given a list of infoboxes, return dictionary with attribute mappings"""
    return {infobox: get_single_mappings(infobox) for infobox in infoboxes}


def get_infoboxes(path):
    """Given path to excel file, return list of infoboxes"""
    return _get_infoboxes(get_infobox_totals(path))


def _get_infoboxes(infobox_totals):
    """Given dictionary with infobox totals, return list of infoboxes"""
    return infobox_totals.keys()


def total_infoboxes(path):
    """Given path to excel file, return total number of infoboxes"""
    return _total_infoboxes(get_infobox_totals(path))


def _total_infoboxes(infobox_totals):
    """Given dictionary with infobox totals, return total number of infoboxes"""
    return len(infobox_totals)


def total_pages(path):
    """Given path to excel file, return total number of wikipedia pages"""
    return _total_pages(get_infobox_totals(path))


def _total_pages(infobox_totals):
    """Given dictionary with infobox totals, return total number of wikipedia pages"""
    return sum(infobox_totals.values())


# WRITING

def write_json(dict, path):
    """Given a dict and a path, save dict to path as json file"""
    with open(path, 'wb') as fp:
        json.dump(dict, fp)


def write_graph(graph, path):
    """Given a graph object and a path, save graph to path as gpickle"""
    nx.write_gpickle(graph, path)
