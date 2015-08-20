import unittest
from wikimap import synonyms


class TestWordNetUtils(unittest.TestCase):

    def test_clean_wordnet(self):
        self.assertEqual(
            synonyms.clean_wordnet(u'Canis_familiaris'), 'canis familiaris')


class TestIdSynset(unittest.TestCase):

    def test_id_synset_single_key(self):
        self.assertItemsEqual(synonyms.id_synset('dog', ['canis familiaris']),
                              ['dog', 'domestic dog', 'canis familiaris'])

    def test_id_synset_single_bad_key(self):
        self.assertRaisesRegexp(
            RuntimeError, "No synset of 'dog' matches keys",
            synonyms.id_synset, 'dog', ['junk'])

    def test_id_synset_bad_primary(self):
        self.assertRaisesRegexp(
            KeyError, "WordNet contains no synsets for word: asdf",
            synonyms.id_synset, 'asdf', ['junk'])

    def test_id_synset_single_insufficient_key(self):
        self.assertRaisesRegexp(
            RuntimeError,
            "Keys insufficient to uniquely identify synset, \d synsets found",
            synonyms.id_synset, 'maintain', ['keep'])

    def test_id_synset_many_keys(self):
        self.assertItemsEqual(synonyms.id_synset('maintain', ['keep', 'hold']),
                              ['keep', 'maintain', 'hold'])

    def test_id_synset_many_insufficient_keys(self):
        self.assertRaisesRegexp(
            RuntimeError,
            "Keys insufficient to uniquely identify synset, \d synsets found",
            synonyms.id_synset, 'maintain', ['keep', 'junk'])

    def test_id_synset_many_oversufficient_keys(self):
        self.assertItemsEqual(
            synonyms.id_synset('maintain', ['conserve', 'preserve']),
            ['conserve', 'preserve', 'maintain', 'keep up'])


class TestSimilarity(unittest.TestCase):
    def test_intersect_ordered(self):
        a = [5,4,3,2,1]
        b = [1,3,5,6]
        # assertEqual not assertItemsEqual b/c order matters
        self.assertEqual(synonyms.intersect_ordered(a, b), [5,3,1])

    def test_similarity_between_same(self):
        self.assertEqual(synonyms.similarity_between('bridge', 'bridge'),
                         ['Bridge', 5, 0, 0])

    def test_similarity_between_at_root(self):
        self.assertEqual(synonyms.similarity_between('station', 'train'),
                         ['owl:Thing', 0, 4, 2])

    def test_similarity_between_one_above(self):
        self.assertEqual(synonyms.similarity_between('bridge', 'tunnel'),
                         ['RouteOfTransportation', 4, 1, 1])

    def test_similarity_between_random(self):
        self.assertEqual(synonyms.similarity_between('church', 'japan-station'),
                         ['ArchitecturalStructure', 2, 2, 3])

    def test_similar_enough_two_above(self):
        # 'Bridge' and 'RailwayStation'
        self.assertTrue(synonyms.similar_enough('bridge', 'japan-station'))
        self.assertTrue(synonyms.similar_enough('japan-station', 'bridge'))

    def test_similar_enough_two_above_diff_levels(self):
        # 'Bridge' and 'Station'
        self.assertTrue(synonyms.similar_enough('bridge', 'station'))
        self.assertTrue(synonyms.similar_enough('station', 'bridge'))
        # 'Lake' and 'River'
        self.assertTrue(synonyms.similar_enough('lake', 'river'))
        self.assertTrue(synonyms.similar_enough('river', 'lake'))

    def test_not_similar_enough_two_above_diff_levels(self):
        # 'River' and 'MountainRange'
        self.assertFalse(synonyms.similar_enough('river', 'mountain-range'))
        self.assertFalse(synonyms.similar_enough('mountain-range', 'river'))

    def test_similar_enough_totally_unrelated(self):
        # 'YearInSpaceflight' and 'SupremeCourtOfTheUnitedStatesCase'
        self.assertFalse(synonyms.similar_enough('year-in-spaceflight', 'scotus-case'))
        self.assertFalse(synonyms.similar_enough('scotus-case', 'year-in-spaceflight'))


class TestParaphrase(unittest.TestCase):

    def test_post_paraphrase_cleanup(self):
        node_list = ['aA !!!!!prev!!!!!', 'next-date', 'A<<!!!!!prev!!!!!',
                     'replace', 'A !!!!!preceded_by!!!!!', 'followed', 'next',
                     'nextcomp', 'succeededa by', 'followedby', 'replaced by',
                     'next tournament', 'aA !!!!!previous!!!!! (previous)',
                     'aA Previous "!!!!!Prev!!!!!"', 'followed by',
                     '<A A !!!!!previous!!!!!', 'successor line', 'heir',
                     'followeda by', 'aA !!!!!previous!!!!!', 'succeeded by',
                     'successor', 'a -a succeededa by', 'next event', 'succeeded',
                     '!!!!!suc-type!!!!!', 'previousattraction', 'became',
                     'replaced', 'replacement', "File: foo"]
        expected_list = ['next-date',
                         'replace', 'followed', 'next',
                         'nextcomp', 'succeededa by', 'followedby', 'replaced by',
                         'next tournament',
                         'followed by',
                         'successor line', 'heir',
                         'followeda by', 'succeeded by',
                         'successor', 'a -a succeededa by', 'next event',
                         'succeeded', 'previousattraction',
                         'became', 'replaced', 'replacement']
        self.assertItemsEqual(synonyms.post_paraphrase_cleanup(node_list, False),
                              expected_list)

    def test_post_paraphrase_cleanup_exclude_unrend(self):
        node_list = ['lid', 'identifiers', 'iata', 'icao', 'wmo', 'faa', 'tc',
                     'gps']

        expected_list = ['identifiers']
        self.assertItemsEqual(synonyms.post_paraphrase_cleanup(node_list, True),
                              expected_list)
