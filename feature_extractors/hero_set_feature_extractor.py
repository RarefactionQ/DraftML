import numpy

from feature_extractors.hero_feature_extractor import HeroFeatureExtractor

class HeroSetFeatureExtractor(object):
    """Extracts features related to a set of heros."""

    def __init__(self):
        super(HeroSetFeatureExtractor, self).__init__()
        self.hfe = HeroFeatureExtractor()

    def extract(self, heroes):
        hero_features = [self.hfe.extract(hero) for hero in heroes]

        features = list()
        for values in zip(*hero_features):
            features.append(sum(values))
            features.append(max(values))
            features.append(min(values))
            features.append(numpy.median(values))
            features.append(numpy.prod(values))

        return features

    def extractFeatureNames(self):
        feature_names = list()
        for feature_name in self.hfe.extractFeatureNames():
            fxns = ["sum", "max", "min", "median", "product"]
            for fxn in fxns:
                feature_names.append("%s_%s" % (fxn, feature_name))

        return feature_names
