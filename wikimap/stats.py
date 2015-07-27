import networkx as nx
import wikimap


def percent_str(part, total):
    """Takes part (float) out of total (float) and returns a string
    with a percent sign at the end representing the percent, rounded
    to two decimal places.
    """
    return str(round(100 * float(part) / float(total), 2)) + '%'


def fraction_msg(msg, missed, total, thing):
    """Takes number of missed (float) out of total (float) of thing
    (str) and returns a string with a statement about how many
    of thing (str) are missed; numbers given in integer form.
    """
    return "{msg} {missed} {thing} out of {total} total, or {percent}".format(
        msg=msg, missed=str(
            int(missed)), thing=thing, total=str(
            int(total)), percent=percent_str(
                missed, total))


def dict_sublength(nest_dict):
    """Returns the sum of all the lengths of one level nested dicts, e.g.
    food_colors = {'fruit': {'orange': 'orange',
                             'apple': 'red',
                             'banana': 'yellow'},
                   'vegetables': {'lettuce': 'green',
                                  'beet': 'red',
                                  'pumpkin': 'orange'}}
    will return 6
    """
    return sum(len(v) for v in nest_dict.itervalues())
