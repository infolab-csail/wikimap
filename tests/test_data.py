import unittest
import mock
import os.path
from wikimap import data


# DISCLAIMER: many of these tests are of functions that are light
# wrappers around core, stable functions in disctributed modules that
# read/write files. Therefore, these tests rely a lot on mocks and
# sometimes may seem to verge more on testing implementation rather
# than abstract functionality, but this is because of the unique
# nature of what is being tested.

class TestReading(unittest.TestCase):

    def test_read_graph(self):
        # read_graph() is a bare-bone wrapper around
        # nx.read_gpickle(), so this test is a little silly
        with mock.patch('nx.read_gpickle') as mock_read:
            fake_graph = "graph"
            fake_path = "path/to/dest"
            mock_read.return_value = fake_graph

            returned = data.read_graph(fake_path)
            expected = fake_graph

            # if nx.read_gpickle() returns a graph, does read_graph
            # return the same graph? (yes I know, a little stupid, but
            # to be 100% covered)
            self.assertEqual(returned, expected)

            # when I call read_graph() with fake_path, does
            # nx.read_gpickle() get called with the same path?
            nx.read_gpickle.assert_called_once_with(fake_path)

    def test_get_infobox_totals(self):
        path = "fake_data/test_infoboxes.xlsx"
        returned = data.get_infobox_totals(path)
        expected = {"Template:Infobox settlement": 354090,
                    "Template:Infobox person": 146915,
                    "Template:Infobox album": 122492,
                    "Template:Infobox football biography": 118713,
                    "Template:Infobox 2011": 5}
        self.assertEqual(returned, expected)

        # test that the dependant file exists, otherwise the assertion
        # is unreliable
        self.assertTrue(os.path.isfile(path))


class TestJSON(unittest.TestCase):

    def setUp(self):
        # set up mock of open()
        patcher = mock.patch('open')
        self.addCleanup(patcher.stop)
        patcher.start()
        fake_file_object = 100
        fake_path = "path/to/dest"
        patcher.return_value = fake_file_object

    def test_write_json(self):
        # write_json() depends on open() and json.dump(), so we are
        # mocking both in this test.
        with mock.patch('json.dump') as mock_dump:
            fake_data = {"Template:Infobox settlement": 354090,
                         "Template:Infobox person": 146915,
                         "Template:Infobox album": 122492,
                         "Template:Infobox football biography": 118713,
                         "Template:Infobox 2011": 5}
            data.write_json(fake_data, fake_path)

            # assume open() returns fake_file_object, does json.dump()
            # get called with the arguments I expect? If so, I trust
            # that json.dump is well tested already.
            json.dump.assert_called_once_with(fake_data, fake_file_object)

            # makes sure write_json() is calling open() correctly,
            # otherwise we can't assume open() returns a valid result
            open.assert_called_once_with(fake_path, 'wb')

    def test_read_json(self):
        # write_json() depends on open() and json.load(), so we are
        # mocking both in this test.
        with mock.patch('json.load') as mock_load:
            fake_data = {"Template:Infobox settlement": 354090,
                         "Template:Infobox person": 146915,
                         "Template:Infobox album": 122492,
                         "Template:Infobox football biography": 118713,
                         "Template:Infobox 2011": 5}
            mock_load.return_value = fake_data

            returned = data.read_json(fake_path)
            expected = fake_data

            # assume open() and write_json() work, does read_json()
            # return what I expect?
            self.assertEquals(returned, expected)

            # assume open() returns fake_file_object, does json.load()
            # get called with the arguments I expect? If so, I trust
            # that json.load is well tested already.
            json.load.assert_called_once_with(fake_file_object)

            # makes sure write_json() is calling open() correctly,
            # otherwise we can't assume open() returns a valid result
            open.assert_called_once_with(fake_path, 'rb')


class TestDependantInfoboxData(unittest.TestCase):

    def setUp(self):
        # set up mock of get_infobox_totals()
        patcher = mock.patch('get_infobox_totals')
        self.addCleanup(patcher.stop)
        patcher.start()
        fake_data = {"Template:Infobox settlement": 354090,
                     "Template:Infobox person": 146915,
                     "Template:Infobox album": 122492,
                     "Template:Infobox football biography": 118713,
                     "Template:Infobox 2011": 5}
        fake_path = "path/to/dest"
        patcher.return_value = fake_data

    def test_mock_get_infobox_totals(self):
        # makes sure that mock of get_infobox_totals() is working as I
        # expect

        returned = get_infobox_totals(fake_path)
        expected = fake_data

        # Does get_infobox_totals() return what I expect? Otherwise,
        # the tests below are not reliable
        self.assertEqual(result, expected)

        # Test that assert_called_once_with() returns my arguments,
        # otherwise the below tests are not reliable
        get_infobox_totals.assert_called_once_with(fake_path)

    def test_get_infoboxes(self):
        # get_infoboxes() depends on get_infobox_totals(), so we are
        # mocking get_infobox_totals() in this test

        returned = data.get_infoboxes(fake_path)
        expected = ["Template:Infobox settlement",
                    "Template:Infobox person",
                    "Template:Infobox album",
                    "Template:Infobox football biography",
                    "Template:Infobox 2011"]

        # assume get_infobox_totals() returns valid result, does
        # get_infoboxes() return what I expect?
        self.assertEqual(returned, expected)

        # makes sure get_infoboxes() is calling get_infobox_totals()
        # correctly, otherwise we can't assume get_infobox_totals()
        # returns a valid result
        get_infobox_totals.assert_called_once_with(fake_path)

    def test_total_infoboxes(self):
        # total_infoboxes() depends on get_infobox_totals(), so we are
        # mocking get_infobox_totals() in this test

        returned = data.total_infoboxes(fake_path)
        expected = 5

        # assume get_infobox_totals() returns valid result, does
        # total_infoboxes() return what I expect?
        self.assertEqual(returned, expected)

        # makes sure total_infoboxes() is calling get_infobox_totals()
        # correctly, otherwise we can't assume get_infobox_totals()
        # returns a valid result
        get_infobox_totals.assert_called_once_with(fake_path)

    def test_total_pages(self):
        # total_pages() depends on get_infobox_totals(), so we are
        # mocking get_infobox_totals() in this test

        returned = data.total_infoboxes(fake_path)
        expected = 354090 + 146915 + 122492 + 118713 + 5

        # assume get_infobox_totals() returns valid result, does
        # total_pages() return what I expect?
        self.assertEqual(returned, expected)

        # makes sure total_pages() is calling get_infobox_totals()
        # correctly, otherwise we can't assume get_infobox_totals()
        # returns a valid result
        get_infobox_totals.assert_called_once_with(fake_path)
