import unittest2

from feature_extractors.team_feature_extractor import TeamFeatureExtractor
from feature_extractors.team_set_feature_extractor import TeamSetFeatureExtractor

class TestTeamSetFeatureExtractor(unittest2.TestCase):
    def setUp(self):
        self.tsfe = TeamSetFeatureExtractor()
        self.tfe = TeamFeatureExtractor()

    def test_output(self):
        output = dict()

        teams = ["EHOME", "Alliance"]

        for name, value in zip(self.tsfe.extractFeatureNames(), self.tsfe.extract(teams)):
            output[name] = value

        self.assertEqual(len(self.tsfe.extractFeatureNames()), len(self.tsfe.extract(teams)))

        self.assertAlmostEqual(output["glicko2 rating_delta"], -65.08)
        self.assertAlmostEqual(output["glicko rating_delta"], 352.44)
        self.assertAlmostEqual(output["elo rating_delta"], 227.04)
