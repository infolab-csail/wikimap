import itertools
import json
from xlrd import open_workbook

### INPUT ###
# add caching decorator
def read_json(path):
    with open(path, 'rb') as fp:
        return json.load(fp)

# add caching decorator
def get_infobox_totals(path):
    wb = open_workbook(path)
    sheet = wb.sheet_by_index(0)

    names = sheet.col_values(0,2) # 0th col, starting at 2nd row
    template_names = ['Template:Infobox ' + str(cell).replace('-', ' ') for cell in names]

    numbers = sheet.col_values(1,2) # 1th col, starting at 2nd row

    return dict(itertools.izip(template_names,numbers))

# add caching decorator
def get_infoboxes(path):
    return infobox_pages(path).keys()

# add caching decorator
def total_infoboxes(path):
    return len(get_infobox_totals(path))

# add caching decorator
def total_pages(path):
    return sum(infobox_pages(path).values())

### OUTPUT ###
def write_json(dict, path):
    with open(path, 'wb') as fp:
        json.dump(dict, fp)
