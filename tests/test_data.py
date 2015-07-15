import unittest
from mock import Mock
from wikimap import data


class TestReading(unittest.TestCase):
    # somehow make sure files exist in data/ directory

    def test_read_json(self):
        # stub

    def test_read_graph(self):
        # stub

    def test_get_infobox_totals(self):
        path = "data/test_infoboxes.xlsx"
        returned = data.get_infobox_totals(path)
        expected = {"Template:Infobox settlement": 354090,
                    "Template:Infobox person": 146915,
                    "Template:Infobox album": 122492,
                    "Template:Infobox football biography": 118713,
                    "Template:Infobox 2011": 5}
        self.assertEqual(returned, expected)


class TestWriting(unittest.TestCase):
    def test_write_json(self):
        # stub

    def tearDown(self):
        # remove files

class TestDependantInfoboxData(unittest.TestCase):
    def setUp(self):
        # set up mock of get_infobox_totals()

    def test_get_infoboxes(self):
        # stub

    def test_total_infoboxes(self):
        # stub

    def test_total_pages(self):
        # stub
