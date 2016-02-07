import unittest2

from feature_extractors.hero_feature_extractor import HeroFeatureExtractor
from feature_extractors.hero_set_feature_extractor import HeroSetFeatureExtractor

class TestHeroSetFeatureExtractor(unittest2.TestCase):
    def setUp(self):
        self.hsfe = HeroSetFeatureExtractor()
        self.hfe = HeroFeatureExtractor()

    def test_output(self):
        output = dict()

        heroes = ["Abaddon", "Arc Warden", "Death Prophet", "Huskar", "Juggernaut"]

        for name, value in zip(self.hsfe.extractFeatureNames(), self.hsfe.extract(heroes)):
            output[name] = value

        self.assertEqual(len(self.hsfe.extractFeatureNames()), len(self.hsfe.extract(heroes)))

        self.assertEqual(output["sum_ATT"], 4)
        self.assertEqual(output["max_ATT"], 2)
        self.assertEqual(output["min_ATT"], 0)
        self.assertEqual(output["median_ATT"], 1)
        self.assertEqual(output["product_ATT"], 0)

        self.assertEqual(output["sum_FARM PRIORITY"], 0.6105)
        self.assertEqual(output["max_FARM PRIORITY"], 0.162)
        self.assertEqual(output["min_FARM PRIORITY"], 0.088)
        self.assertEqual(output["median_FARM PRIORITY"], 0.1301)
        self.assertEqual(output["product_FARM PRIORITY"], 2.3999519522879996e-05)
