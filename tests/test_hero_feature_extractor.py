import unittest2

from feature_extractors.hero_feature_extractor import HeroFeatureExtractor

class TestHeroFeatureExtractor(unittest2.TestCase):
    def setUp(self):
        self.hfe = HeroFeatureExtractor()

    def test_output(self):
        output = dict()

        for name, value in zip(self.hfe.extractFeatureNames(), self.hfe.extract("Abaddon")):
            output[name] = value

        self.assertEqual(output["ATT"], STR)
        self.assertEqual(output["STR"], 23)
        self.assertEqual(output["HP/S"], 0.25)


#        HERO,ATT,STR,STR+,AGI,AGI+,INT,INT+,T,T+,LVL 25,MOV,AR,DMG MIN,DMG MAX,RNG,BAT,ATKPT,ATKBS,VIS-D,VIS-N,TURN,COLL,HP/S
#Abaddon,STR,23,2.7,17,1.5,21,2,61,6.2,216,310,1.38,55,65,128,1.7,0.56,0.41,1800,800,0.6,24,0.25

