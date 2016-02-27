import unittest2

from feature_extractors.team_feature_extractor import TeamFeatureExtractor

class TestTeamFeatureExtractor(unittest2.TestCase):
    def setUp(self):
        self.tfe = TeamFeatureExtractor()

    def test_output(self):
        output = dict()

        for name, value in zip(self.tfe.extractFeatureNames(), self.tfe.extract("EHOME")):
            output[name] = value

        self.assertEqual(len(self.tfe.extractFeatureNames()), len(self.tfe.extract("EHOME")))

        self.assertEqual(output["country"], "China")
        self.assertEqual(output["wins"], 189)
        self.assertEqual(output["losses"], 134)
        self.assertEqual(output["glicko2 rating"], 1840.65)
        self.assertEqual(output["elo rating"], 1256.75)
