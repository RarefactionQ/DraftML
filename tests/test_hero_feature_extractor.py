import unittest2

from feature_extractors.hero_feature_extractor import HeroFeatureExtractor

class TestHeroFeatureExtractor(unittest2.TestCase):
    def setUp(self):
        self.hfe = HeroFeatureExtractor()

    def test_output(self):
        output = dict()

        for name, value in zip(self.hfe.extractFeatureNames(), self.hfe.extract("Abaddon")):
            output[name] = value

        self.assertEqual(len(self.hfe.extractFeatureNames()), len(self.hfe.extract("Abaddon")))

        self.assertEqual(output["STR"], 23)
        self.assertEqual(output["STR+"], 2.7)
        self.assertEqual(output["HP/S"], 0.25)
        self.assertEqual(output["LVL 25"], 216)

        self.assertEqual(output["FARM PRIORITY"], 0.088)
