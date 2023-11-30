"""Match model with helpers of calculate ELO rank"""
from models.player import Player, Teams
from config.exceptions import EloException

class Match:
    """Match Class"""

    def __init__(self, game_id: int, players: list[Player]):
        self.game_id = game_id
        self.opponents = {
            "winner_team": None,
            Teams.RED.value: {
                "players": [],
                "team_points": 0,
                "match_points": 0,
                "match_score": None,
                "expected_score": None
            },
            Teams.BLUE.value: {
                "players": [],
                "team_points": 0,
                "match_points": 0,
                "match_score": None,
                "expected_score": None
            }
        }

        for player in players:
            self.opponents[player.team]["players"].append(player)
            self.opponents[player.team]["team_points"] += player.rank_score

    def set_expected_score(self, team: Teams, expected_score):
        """set expected score value"""
        self.opponents[team]["expected_score"] = expected_score

    def get_expected_score(self, team: Teams):
        """get expected_score value"""
        return self.opponents[team]["expected_score"]

    def get_team_points(self, team: Teams):
        """return the total rank score of a team players"""
        return self.opponents[team]["team_points"]

    def finish(self, score: (int, int)):
        """set result of the match"""

        self.opponents["winner_team"] = Teams.RED.value if score[0] > score[1] else Teams.BLUE.value

        self.opponents[Teams.RED.value]["match_score"] = score[0]
        self.opponents[Teams.BLUE.value]["match_score"] = score[1]

    def set_match_points(self, points: (int, int)):
        """calculate points of the finished game"""

        self.opponents[Teams.RED.value]["match_points"] = points[0]
        self.opponents[Teams.BLUE.value]["match_points"] = points[1]


    def get_winner_opponent(self):
        """retrieve the winner opponent of the match"""
        if self.opponents["winner_team"] is None:
            raise EloException("No winner team available")

        return self.opponents[self.opponents["winner_team"]]
