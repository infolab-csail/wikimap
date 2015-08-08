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

    def tes_id_synset_many_oversufficient_keys(self):
        self.assertItemsEqual(
            synonyms.id_synset('maintain', ['conserve', 'preserve']),
            ['conserve', 'preserve', 'maintain', 'keep up'])
