import csv
import re

class HeroFeatureExtractor(object):
    """Extract features related to a hero."""

    def __init__(self):
        super(HeroFeatureExtractor, self).__init__()
        self.heroes = dict()
        with open('data/heroes.csv', 'r') as f:
            heroreader = csv.reader(f)
            for hero in heroreader:
                self.heroes[self.clean_hero_name(hero[0])] = hero[1:]

    def clean_hero_name(self, hero_name_str):
        return re.sub('[^A-Za-z0-9]+', '', hero_name_str)

    def extract(self, hero_name_str):
        """Returns attributes related to a particular hero."""
        features = list()

        features.extend(self.getHeroStats(self.clean_hero_name(hero_name_str)))

        return features


    def getHeroStats(self, hero_name_str):
        """Returns the index of the hero in the hero list."""
        return [float(n) for n in self.heroes[hero_name_str][1:]]
