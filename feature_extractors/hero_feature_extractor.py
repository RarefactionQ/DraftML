import csv
import re

class HeroFeatureExtractor(object):
    """Extract features related to a hero."""

    def __init__(self):
        super(HeroFeatureExtractor, self).__init__()

        self.hero_stats = dict()
        with open('data/heroes.csv', 'r') as f:
            reader = csv.reader(f)
            self.hero_stats["names"] = reader.next()
            for hero in reader:
                self.hero_stats[self.clean_hero_name(hero[0])] = hero[1:]

        self.farm_priorities = dict()
        with open('data/farm_priority.csv', 'rU') as f:
            reader = csv.reader(f)
            self.farm_priorities["names"] = reader.next()
            for hero in reader:
                self.farm_priorities[self.clean_hero_name(hero[0])] = hero[1:]

    def clean_hero_name(self, hero_name_str):
        return re.sub('[^A-Za-z0-9]+', '', hero_name_str)

    def extract(self, hero_name_str):
        """Returns attributes related to a particular hero."""

        clean_hero_name = self.clean_hero_name(hero_name_str)

        features = list()
        features.extend(self.getHeroStats(clean_hero_name))
        features.extend(self.getHeroFarmPriority(clean_hero_name))
        return features

    def extractFeatureNames(self):
        """Returns feature names"""

        features = list()
        features.extend(self.getHeroStatsNames())
        features.extend(self.getHeroFarmPriorityNames())
        return features

    def getHeroFarmPriority(self, hero_name_str):
        return [float(n) for n in self.farm_priorities[hero_name_str][0:]]

    def getHeroFarmPriorityNames(self):
        return self.farm_priorities["names"][1:]

    def getHeroStats(self, hero_name_str):
        return [float(n) for n in self.hero_stats[hero_name_str][0:]]

    def getHeroStatsNames(self):
        return self.hero_stats["names"][1:]

