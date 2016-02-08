import random

class OracleFeatureExtractor(object):
    """Extracts features related to a match with amazing predictive power."""

    def extract(self, winner):
        """winner is 1 or 0"""
        return [(random.random() + winner) / 2]

    def extractFeatureNames(self):
        return ["fuzzy_oracle"]
