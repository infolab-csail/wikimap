import unittest
from wikimap import graph
import networkx.testing as nxt
import networkx as nx


class TestGeneralNetworkMethods(unittest.TestCase):

    def setUp(self):
        self.G = graph.WikiMap()

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

        # EXPECTED:
        # three node group
        self.expected_three1 = graph.WikiMap()
        self.expected_three1.add_edge("Y", "X")
        self.expected_three1.add_edge("X", "Y")
        self.expected_three1.add_edge("Z", "X")
        self.expected_three1.add_edge("X", "Z")

        # three node group (another)
        self.expected_three2 = graph.WikiMap()
        self.expected_three2.add_edge("alpha", "beta")
        self.expected_three2.add_edge("beta", "alpha")
        self.expected_three2.add_edge("alpha", "gamma")
        self.expected_three2.add_edge("gamma", "alpha")

        # four node group
        self.expected_four = graph.WikiMap()
        self.expected_four.add_edge("A", "B")
        self.expected_four.add_edge("B", "A")
        self.expected_four.add_edge("A", "C")
        self.expected_four.add_edge("C", "A")
        self.expected_four.add_edge("D", "C")
        self.expected_four.add_edge("C", "D")
        # because directionality of graph lost in process

    def test_connected_component_lengths(self):
        self.assertItemsEqual(
            self.G.connected_component_lengths(), [2, 3, 3, 4])

    def test_connected_component_statistics(self):
        self.assertItemsEqual(
            self.G.connected_component_statistics(), {2: 1, 3: 2, 4: 1})

    def test_connected_components_with_size(self):
        self.assertEqual(len(self.G.connected_components_with_size(3)),
                         len([self.expected_three1, self.expected_three2]))
        # unfortunately cannot test that two lists of graphs are
        # equal, so only test length of lists here, and then that the
        # graph in the list of len=1 below is equal. Hopefully this is
        # enough.

        returned_four = self.G.connected_components_with_size(4)[0]
        nxt.assert_graphs_equal(returned_four, self.expected_four)

    def test_connected_component_with_node(self):
        # "X" is a hub
        returned_three1 = self.G.connected_component_with_node("X")
        nxt.assert_graphs_equal(returned_three1, self.expected_three1)

        # "beta" is not a hub
        returned_three2 = self.G.connected_component_with_node("beta")
        nxt.assert_graphs_equal(returned_three2, self.expected_three2)

        # "A" is a hub
        returned_four = self.G.connected_component_with_node("A")
        nxt.assert_graphs_equal(returned_four, self.expected_four)

    def test_connected_component_with_node_not_found(self):
        self.assertRaisesRegexp(
            nx.exception.NetworkXError, "Node \"junk\" not in graph",
            self.G.connected_component_with_node, "junk")


class TestCleaningNodes(unittest.TestCase):

    def test_clean_skips(self):
        self.assertEqual(graph.WikiMap.clean("File: foo"), "File: foo")
        self.assertEqual(
            graph.WikiMap.clean("!!!!!foo!!!!!"), "!!!!!foo!!!!!")

    def test_clean_unicode(self):
        self.assertEqual(
            graph.WikiMap.clean(u'Rate\xa0of\xa0fire'), "rate of fire")

    def test_clean_punct_remove(self):
        # capitalization and punctuation removal
        self.assertEqual(graph.WikiMap.clean("Heights"), "heights")
        self.assertEqual(
            graph.WikiMap.clean("discovery_site"), "discovery site")
        self.assertEqual(graph.WikiMap.clean("Max. devices"), "max devices")
        self.assertEqual(graph.WikiMap.clean("Circus tent?"), "circus tent")
        self.assertEqual(graph.WikiMap.clean("Web site:"), "web site")
        self.assertEqual(graph.WikiMap.clean("/Karaoke"), "karaoke")

    def test_clean_punct_except(self):
        # exception to punctuation removal
        self.assertEqual(graph.WikiMap.clean("% of total exports"),
                         "% of total exports")
        self.assertEqual(graph.WikiMap.clean("Managing editor, design"),
                         "managing editor, design")
        self.assertEqual(graph.WikiMap.clean("MSRP US$"), "msrp us$")
        self.assertEqual(graph.WikiMap.clean("Specific traits & abilities"),
                         "specific traits & abilities")
        self.assertEqual(graph.WikiMap.clean("re-issuing"), "re-issuing")
        # another good example: "Capital-in-exile"

    def test_clean_HTML_remove(self):
        # HTML-like junk removal
        self.assertEqual(graph.WikiMap.clean("<hiero>G16</hiero>"), "g16")
        self.assertEqual(graph.WikiMap.clean("&mdot;foo"), "foo")
        self.assertEqual(graph.WikiMap.clean("Opened</th>"), "opened")

    def test_clean_parens(self):
        self.assertEqual(
            graph.WikiMap.clean("Parent club(s)"), "parent club")
        self.assertEqual(
            graph.WikiMap.clean("Team president (men)"), "team president")
        self.assertEqual(graph.WikiMap.clean("Deaconess(es)"), "deaconess")
        self.assertEqual(graph.WikiMap.clean("ARWU[5]"), "arwu")

    def test_clean_possessive(self):
        self.assertEqual(
            graph.WikiMap.clean("Women's coach"), "women's coach")
        self.assertEqual(
            graph.WikiMap.clean("Teams' champion"), "teams' champion")


class TestAddToField(unittest.TestCase):

    def setUp(self):
        self.test_dict = ["bannana", {"foo": ["bar"]}]

    def test_add_to_existing_field_new(self):
        graph.WikiMap.add_to_field(self.test_dict[1], "foo", "aba")
        self.assertItemsEqual(self.test_dict[1], {"foo": ["bar", "aba"]})

    def test_add_to_existing_field_existing(self):
        graph.WikiMap.add_to_field(self.test_dict[1], "foo", "bar")
        self.assertItemsEqual(self.test_dict[1], {"foo": ["bar"]})

    def test_add_to_new_field(self):
        graph.WikiMap.add_to_field(self.test_dict[1], "bar", "aba")
        self.assertItemsEqual(
            self.test_dict[1], {"foo": ["bar"], "bar": ["aba"]})

    def test_add_to_new_location(self):
        self.test_dict[1]['infobox'] = {}
        graph.WikiMap.add_to_field(
            self.test_dict[1]['infobox'], "bar", "aba")
        self.assertItemsEqual(self.test_dict[1], {"foo": ["bar"],
                                                  "infobox": {"bar": ["aba"]}})


class TestInsertingInformation(unittest.TestCase):

    def setUp(self):
        self.G = graph.WikiMap()

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
        self.G = graph.WikiMap()
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


class TestAnalytics(unittest.TestCase):
    def test_connected_component_nodes_with_size(self):
        G = graph.WikiMap()

        # four node group
        G.add_edge("A", "B")
        G.add_edge("A", "C")
        G.add_edge("D", "C")

        # three node group
        G.add_edge("Y", "X")
        G.add_edge("Z", "X")

        # three node group (another)
        G.add_edge("alpha", "beta")
        G.add_edge("alpha", "gamma")

        # two node group
        G.add_edge("M", "N")

        self.assertItemsEqual(G.connected_component_nodes_with_size(3),
                              [["Y", "X", "Z"], ["alpha", "beta", "gamma"]])
