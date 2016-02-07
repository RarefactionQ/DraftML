import unittest2

from feature_extractors.hero_set_feature_extractor import HeroSetFeatureExtractor

class TestHeroSetFeatureExtractor(unittest2.TestCase):
    def setUp(self):
        self.hsfe = HeroSetFeatureExtractor()

    def test_output(self):
        output = dict()

        heroes = ["Abaddon", "Arc Warden", "Death Prophet", "Huskar", "Juggernaut"]

        for name, value in zip(self.hsfe.extractFeatureNames(), self.hsfe.extract(heroes)):
            output[name] = value

        self.assertEqual(len(self.hsfe.extractFeatureNames()), len(self.hsfe.extract(heroes)))

