import csv

class TeamFeatureExtractor(object):
    """Extract features related to a team."""

    NULL_VALUE = 0

    def __init__(self):
        super(TeamFeatureExtractor, self).__init__()

        self.team_stats = dict()
        with open('data/teams.csv', 'rU') as f:
            reader = csv.reader(f)
            self.team_stats["names"] = reader.next()[1:]
            for team in reader:
                self.team_stats[team[1]] = team[2:] # 0 is rank, 1 is team name

    def extract(self, team_name_str):
        """Returns attributes related to a particular team."""
        return self.getTeamStats(team_name_str)

    def extractFeatureNames(self):
        """Returns feature names"""
        return self.getTeamStatsNames()

    def getTeamStats(self, team_name_str):
        try:
            return [self.conform(n) for n in self.team_stats[team_name_str][0:]]
        except KeyError:
            return self.getTeamStatsUnknownTeam()

    def getTeamStatsNames(self):
        return self.team_stats["names"][1:] # now 0 is team name

    def conform(self, value):
        try:
            return float(value)
        except ValueError:
            return self.NULL_VALUE

    def getTeamStatsUnknownTeam(self):
        return [self.NULL_VALUE for n in xrange(len(self.getTeamStatsNames()))]
