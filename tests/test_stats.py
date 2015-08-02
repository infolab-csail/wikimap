import unittest
from wikimap import stats


class TestStats(unittest.TestCase):

    def test_percent_str(self):
        self.assertEqual(stats.percent_str(1, 3), "33.33%")
        self.assertEqual(stats.percent_str(2, 4), "50.0%")
        self.assertEqual(stats.percent_str(2, 3), "66.67%")

    def test_fraction_msg(self):
        self.assertEqual(stats.fraction_msg("There are", 2.0, 4.0, "test things"),
                         "There are 2 test things out of 4 total, or 50.0%")

    def test_dict_sublength(self):
        food_colors = {'fruit': {'orange': 'orange',
                                 'apple': 'red',
                                 'banana': 'yellow'},
                       'vegetables': {'lettuce': 'green',
                                      'beet': 'red',
                                      'pumpkin': 'orange'}}

        self.assertEqual(stats.dict_sublength(food_colors), 6)
