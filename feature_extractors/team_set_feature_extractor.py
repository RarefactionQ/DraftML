import numpy

from feature_extractors.team_feature_extractor import TeamFeatureExtractor

class TeamSetFeatureExtractor(object):
    """Extracts features related to a set of heros."""

    FEATURES_TO_DELTA = ["glicko2 rating", "glicko rating", "elo rating"]

    def __init__(self):
        super(TeamSetFeatureExtractor, self).__init__()
        self.tfe = TeamFeatureExtractor()

    def extract(self, teams):
        team_features = dict()
        team_features[0] = self.tfe.extract(teams[0])
        team_features[1] = self.tfe.extract(teams[1])

        features = list()
        for feature in self.FEATURES_TO_DELTA:
            index = self.tfe.extractFeatureNames().index(feature)
            delta = team_features[1][index] - team_features[0][index]
            features.append(delta)

        return features

    def extractFeatureNames(self):
        feature_names = [feature + "_delta" for feature in self.FEATURES_TO_DELTA]
        return feature_names
