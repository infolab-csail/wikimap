import unittest
from wikimap import wikimap
import networkx.testing as nxt
import networkx as nx


class TestGeneralNetworkMethods(unittest.TestCase):

    def setUp(self):
        self.G = wikimap.WikiMap()

        # four node group
        self.G.add_edge("A", "B")
        self.G.add_edge("A", "C")
        self.G.add_edge("D", "C")

        # three node group
        self.G.add_edge("Y", "X")
        self.G.add_edge("Z", "X")

        # three node group (another)
        self.G.add_edge("alpha", "beta")
        self.G.add_edge("alpha", "gamma")

        # two node group
        self.G.add_edge("M", "N")

    def test_connected_component_lengths(self):
        self.assertItemsEqual(
            self.G.connected_component_lengths(), [2, 3, 3, 4])

    def test_connected_component_statistics(self):
        self.assertItemsEqual(
            self.G.connected_component_statistics(), {2: 1, 3: 2, 4: 1})

    def test_connected_components_with_size(self):
        # three node group
        expected_three1 = wikimap.WikiMap()
        expected_three1.add_edge("Y", "X")
        expected_three1.add_edge("Z", "X")

        # three node group (another)
        expected_three2 = wikimap.WikiMap()
        expected_three2.add_edge("alpha", "beta")
        expected_three2.add_edge("alpha", "gamma")

        # four node group
        expected_four = wikimap.WikiMap()
        expected_four.add_edge("A", "B")
        expected_four.add_edge("B", "A")
        expected_four.add_edge("A", "C")
        expected_four.add_edge("C", "A")
        expected_four.add_edge("D", "C")
        expected_four.add_edge("C", "D")
        # because directionality of graph lost in process

        self.assertEqual(len(self.G.connected_components_with_size(3)),
                         len([expected_three1, expected_three2]))
        # unfortunately cannot test that two lists of graphs are
        # equal, so only test length of lists here, and then that the
        # graph in the list of len=1 below is equal. Hopefully this is
        # enough.

        returned_four = self.G.connected_components_with_size(4)[0]
        nxt.assert_graphs_equal(returned_four, expected_four)


class TestCleaningNodes(unittest.TestCase):

    def test_clean_skips(self):
        self.assertEqual(wikimap.WikiMap.clean("File: foo"), "File: foo")
        self.assertEqual(
            wikimap.WikiMap.clean("!!!!!foo!!!!!"), "!!!!!foo!!!!!")

    def test_clean_unicode(self):
        self.assertEqual(
            wikimap.WikiMap.clean(u'Rate\xa0of\xa0fire'), "rate of fire")

    def test_clean_punct_remove(self):
        # capitalization and punctuation removal
        self.assertEqual(wikimap.WikiMap.clean("Heights"), "heights")
        self.assertEqual(
            wikimap.WikiMap.clean("discovery_site"), "discovery site")
        self.assertEqual(wikimap.WikiMap.clean("Max. devices"), "max devices")
        self.assertEqual(wikimap.WikiMap.clean("Circus tent?"), "circus tent")
        self.assertEqual(wikimap.WikiMap.clean("Web site:"), "web site")
        self.assertEqual(wikimap.WikiMap.clean("/Karaoke"), "karaoke")

    def test_clean_punct_except(self):
        # exception to punctuation removal
        self.assertEqual(wikimap.WikiMap.clean("% of total exports"),
                         "% of total exports")
        self.assertEqual(wikimap.WikiMap.clean("Managing editor, design"),
                         "managing editor, design")
        self.assertEqual(wikimap.WikiMap.clean("MSRP US$"), "msrp us$")
        self.assertEqual(wikimap.WikiMap.clean("Specific traits & abilities"),
                         "specific traits & abilities")
        self.assertEqual(wikimap.WikiMap.clean("re-issuing"), "re-issuing")
        # another good example: "Capital-in-exile"

    def test_clean_HTML_remove(self):
        # HTML-like junk removal
        self.assertEqual(wikimap.WikiMap.clean("<hiero>G16</hiero>"), "g16")
        self.assertEqual(wikimap.WikiMap.clean("&mdot;foo"), "foo")
        self.assertEqual(wikimap.WikiMap.clean("Opened</th>"), "opened")

    def test_clean_parens(self):
        self.assertEqual(
            wikimap.WikiMap.clean("Parent club(s)"), "parent club")
        self.assertEqual(
            wikimap.WikiMap.clean("Team president (men)"), "team president")
        self.assertEqual(wikimap.WikiMap.clean("Deaconess(es)"), "deaconess")
        self.assertEqual(wikimap.WikiMap.clean("ARWU[5]"), "arwu")

    def test_clean_possessive(self):
        self.assertEqual(
            wikimap.WikiMap.clean("Women's coach"), "women's coach")
        self.assertEqual(
            wikimap.WikiMap.clean("Teams' champion"), "teams' champion")


class TestAddToField(unittest.TestCase):

    def setUp(self):
        self.test_dict = ["bannana", {"foo": ["bar"]}]

    def test_add_to_existing_field_new(self):
        wikimap.WikiMap.add_to_field(self.test_dict[1], "foo", "aba")
        self.assertItemsEqual(self.test_dict[1], {"foo": ["bar", "aba"]})

    def test_add_to_existing_field_existing(self):
        wikimap.WikiMap.add_to_field(self.test_dict[1], "foo", "bar")
        self.assertItemsEqual(self.test_dict[1], {"foo": ["bar"]})

    def test_add_to_new_field(self):
        wikimap.WikiMap.add_to_field(self.test_dict[1], "bar", "aba")
        self.assertItemsEqual(
            self.test_dict[1], {"foo": ["bar"], "bar": ["aba"]})

    def test_add_to_new_location(self):
        self.test_dict[1]['infobox'] = {}
        wikimap.WikiMap.add_to_field(
            self.test_dict[1]['infobox'], "bar", "aba")
        self.assertItemsEqual(self.test_dict[1], {"foo": ["bar"],
                                                  "infobox": {"bar": ["aba"]}})


class TestInsertingInformation(unittest.TestCase):

    def setUp(self):
        self.G = wikimap.WikiMap()

    def test_add_uncleaned(self):
        self.G.add_uncleaned('_unrend_', '_rend_')
        self.G.add_uncleaned('#unrend#', '_rend_')

        self.assertItemsEqual(self.G.nodes(), ['unrend', 'rend'])

        self.assertItemsEqual(
            self.G.node['unrend']['was'], ['_unrend_', '#unrend#'])
        self.assertItemsEqual(self.G.node['rend']['was'], ['_rend_'])

    def test_add_rendering_no_both(self):
        self.G.add_edge('unrend', 'hybrid')
        self.G.add_edge('hybrid', 'rend')

        self.G.add_rendering('Infobox foo bar', 'unrend', 'hybrid')
        self.G.add_rendering('Infobox baz bang', 'hybrid', 'rend')

        self.assertItemsEqual(self.G.node['unrend']['infobox'],
                              {'Infobox foo bar': ['unrend']})

        self.assertItemsEqual(self.G.node['hybrid']['infobox'],
                              {'Infobox foo bar': ['rend'],
                               'Infobox baz bang': ['unrend']})

        self.assertItemsEqual(self.G.node['rend']['infobox'],
                              {'Infobox baz bang': ['rend']})

    def test_add_rendering_with_both(self):
        self.G.add_edge('unrend', 'hybrid')
        self.G.add_edge('hybrid', 'rend')

        self.G.add_rendering('Infobox foo bar', 'unrend', 'hybrid')
        self.G.add_rendering('Infobox foo bar', 'hybrid', 'rend')

        self.assertItemsEqual(self.G.node['unrend']['infobox'],
                              {'Infobox foo bar': ['unrend']})

        self.assertItemsEqual(self.G.node['hybrid']['infobox'],
                              {'Infobox foo bar': ['unrend', 'rend']})

        self.assertItemsEqual(self.G.node['rend']['infobox'],
                              {'Infobox foo bar': ['rend']})

    def test_add_infobox(self):
        self.G.add_edge('unrend', 'rend')

        self.G.add_infobox('Infobox foo bar', 'unrend', 'rend')
        self.G.add_infobox('Infobox baz bang', 'unrend', 'rend')

        self.assertItemsEqual(self.G.edge['unrend']['rend']['infobox'],
                              ['Infobox foo bar', 'Infobox baz bang'])

    def test_add_mapping_no_clean(self):
        self.G.add_mapping('Infobox foo bar', 'unrend', 'rend', False)

        self.assertItemsEqual(self.G.nodes(), ['unrend', 'rend'])
        self.assertItemsEqual(self.G.edges(), [('unrend', 'rend')])

        self.assertItemsEqual(self.G.node['unrend']['infobox'],
                              {'Infobox foo bar': ['unrend']})
        self.assertItemsEqual(self.G.node['rend']['infobox'],
                              {'Infobox foo bar': ['rend']})

        self.assertItemsEqual(self.G.edge['unrend']['rend']['infobox'],
                              ['Infobox foo bar'])

    def test_add_mapping_with_clean(self):
        self.G.add_mapping('Infobox foo bar', '_unrend_', '_rend_', True)

        self.assertItemsEqual(self.G.nodes(), ['unrend', 'rend'])
        self.assertItemsEqual(self.G.edges(), [('unrend', 'rend')])

        self.assertItemsEqual(self.G.node['unrend']['infobox'],
                              {'Infobox foo bar': ['unrend']})
        self.assertItemsEqual(self.G.node['rend']['infobox'],
                              {'Infobox foo bar': ['rend']})

        self.assertItemsEqual(self.G.edge['unrend']['rend']['infobox'],
                              ['Infobox foo bar'])

        self.assertItemsEqual(self.G.node['unrend']['was'], ['_unrend_'])
        self.assertItemsEqual(self.G.node['rend']['was'], ['_rend_'])


class TestFetchingInformation(unittest.TestCase):

    def setUp(self):
        self.G = wikimap.WikiMap()
        self.G.add_edge('unrend', 'hybrid')
        self.G.add_edge('hybrid', 'rend')

        self.G.node['unrend']['was'] = ['_unrend_']
        self.G.node['hybrid']['was'] = ['#hybrid#', '_hybrid_']
        self.G.node['rend']['was'] = ['_rend_']

        self.G.node['unrend']['infobox'] = {'Infobox foo bar': ['unrend']}
        self.G.node['hybrid']['infobox'] = {'Infobox foo bar': ['rend'],
                                            'Infobox baz bang': ['unrend', 'rend']}
        self.G.node['rend']['infobox'] = {'Infobox baz bang': ['rend']}

        self.G.edge['unrend']['hybrid']['infobox'] = ['Infobox foo bar']
        self.G.edge['hybrid']['rend']['infobox'] = ['Infobox baz bang',
                                                    'Infobox aba zaba']

    def test_infoboxes_of_graph_node(self):
        self.assertItemsEqual(self.G.infoboxes_of_graph_node('unrend'),
                              ['Infobox foo bar'])
        self.assertItemsEqual(self.G.infoboxes_of_graph_node('hybrid'),
                              ['Infobox foo bar', 'Infobox baz bang'])

    def test_infoboxes_of_graph(self):
        self.assertItemsEqual(self.G.infoboxes_of_graph(),
                              ['Infobox foo bar', 'Infobox baz bang'])

    def test_rendering_of_graph_node(self):
        self.assertEqual(self.G.rendering_of_graph_node('unrend'), 'unrend')
        self.assertEqual(self.G.rendering_of_graph_node('hybrid'), 'mixed')
        self.assertEqual(self.G.rendering_of_graph_node('rend'), 'rend')

    def test_infoboxes_of_pair(self):
        self.assertItemsEqual(self.G.infoboxes_of_pair('unrend', 'hybrid'),
                              ['Infobox foo bar'])
        self.assertItemsEqual(self.G.infoboxes_of_pair('hybrid', 'rend'),
                              ['Infobox baz bang', 'Infobox aba zaba'])
