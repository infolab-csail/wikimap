import unittest
import os.path
from wikimap import data


class TestInfoboxData(unittest.TestCase):

    def setUp(self):
        self.fake_data = {"Template:Infobox settlement": 354090.0,
                          "Template:Infobox person": 146915.0,
                          "Template:Infobox album": 122492.0,
                          "Template:Infobox football biography": 118713.0,
                          "Template:Infobox 2011": 5.0}

    def test_get_infobox_totals(self):
        path = "tests/fake_data/test_infoboxes.xlsx"

        self.assertEqual(data.get_infobox_totals(path), self.fake_data)

        # make sure the file is actually there
        self.assertTrue(os.path.isfile(path))

    def test_get_infoboxes(self):
        infoboxes = ["Template:Infobox settlement",
                     "Template:Infobox person",
                     "Template:Infobox album",
                     "Template:Infobox football biography",
                     "Template:Infobox 2011"]

        self.assertItemsEqual(data._get_infoboxes(self.fake_data), infoboxes)

    def test_total_infoboxes(self):
        total_infoboxes = 5

        self.assertEqual(data._total_infoboxes(self.fake_data), total_infoboxes)

    def test_total_pages(self):
        total_pages = 354090.0 + 146915.0 + 122492.0 + 118713.0 + 5.0

        self.assertEqual(data._total_pages(self.fake_data), total_pages)
