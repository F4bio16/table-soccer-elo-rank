"""Match model with helpers of calculate ELO rank"""
import datetime
import json

from models.player import Player, Teams
from models.player_score import PlayerScore

from config.exceptions import EloException

class Match:
    """Match Class"""
    state = None
    final_result = None
    expected_score = None

    initial_users_score = None
    delta_users_score = None

    created_at = None
    end_at = None

    args = None
    match_duration = None

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

    @staticmethod
    def get_instance(
        _id: int,
        state,
        final_result,
        expected_score
    ):
        """get match instance"""
        match = Match(_id, [])
        match.state = state
        match.final_result = final_result

        if expected_score is not None:
            str_expected_score = expected_score.split("|")
            match.set_expected_score(Teams.RED.value, float(str_expected_score[0]))
            match.set_expected_score(Teams.BLUE.value, float(str_expected_score[1]))

        return match

    def set_player(self, player: Player, team: Teams, user_game):
        """set player"""

        _team = None
        if team is None:
            _team = player.team
        else:
            _team = team

        if user_game is None:
            self.opponents[_team]["players"].append(player)
        else:
            player_score = PlayerScore(player, user_game)
            self.opponents[_team]["players"].append(player_score)

        self.opponents[_team]["team_points"] += player.rank_score

    def set_expected_score(self, team: Teams, expected_score):
        """set expected score value"""
        self.opponents[team]["expected_score"] = expected_score

    def get_expected_score(self, team: Teams):
        """get expected_score value"""
        return self.opponents[team]["expected_score"]

    def get_team_points(self, team: Teams):
        """return the total rank score of a team players"""
        return self.opponents[team]["team_points"]

    def set_durations(self, created_at, end_at):
        """set match dates"""
        if created_at is not None:
            self.created_at = datetime.datetime.fromisoformat(created_at)
        if end_at is not None:
            self.end_at = datetime.datetime.fromtimestamp(end_at)

        if (self.created_at is not None and self.end_at is not None):
            self.match_duration = self.end_at - self.created_at

    def set_args(self, args):
        """set match args"""
        self.args = json.loads(args) if args is not None else None

    def finish(self, score: (int, int)):
        """set result of the match"""

        self.opponents["winner_team"] = Teams.RED.value if score[0] > score[1] else Teams.BLUE.value

        self.end_at = datetime.datetime.now()
        self.opponents[Teams.RED.value]["match_score"] = score[0]
        self.opponents[Teams.BLUE.value]["match_score"] = score[1]

    def set_match_points(self, points: (int, int)):
        """calculate points of the finished game"""

        self.opponents[Teams.RED.value]["match_points"] = points[0]
        self.opponents[Teams.BLUE.value]["match_points"] = points[1]

    def get_match_points(self, team: Teams):
        """return the points earned with the match"""

        return self.opponents[team]["match_points"]

    def get_winner_opponent(self):
        """retrieve the winner opponent of the match"""
        if self.opponents["winner_team"] is None:
            raise EloException("No winner team available")

        return self.opponents[self.opponents["winner_team"]]
