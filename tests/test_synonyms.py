import unittest
from wikimap import synonyms


class TestWordNetUtils(unittest.TestCase):

    def test_clean_wordnet(self):
        self.assertEqual(
            synonyms._clean_wordnet(u'Canis_familiaris'), 'canis familiaris')

    def test_id_synset_single_key(self):
        self.assertItemsEqual(synonyms.id_synset('dog', ['canis familiaris']),
                              ['dog', 'domestic dog', 'canis familiaris'])

    def test_id_synset_single_insufficient_key(self):
        self.assertRaises(
            RuntimeError, synonyms.id_synset, 'maintain', ['keep'])

    def test_id_synset_many_keys(self):
        self.assertItemsEqual(synonyms.id_synset('maintain', ['keep', 'hold']),
                              ['keep', 'maintain', 'hold'])

    def test_id_synset_many_insufficient_keys(self):
        self.assertRaises(
            RuntimeError, synonyms.id_synset, 'maintain', ['keep', 'junk'])

    def tes_id_synset_many_oversufficient_keys(self):
        self.assertItemsEqual(
            synonyms.id_synset('maintain', ['conserve', 'preserve']),
            ['conserve', 'preserve', 'maintain', 'keep up'])
