"""player model"""
from enum import Enum
from models.user import User

class Teams(Enum):
    """enumeration for Player.team values"""
    RED = '__red__'
    BLUE = '__blue__'

class Player(User):
    """Player Class extended by User"""

    def __init__(self, _id, name, surname, team: Teams, rank_score, last_results, rank_position = None):
        super().__init__(_id=_id,name=name,surname=surname)

        self.team: Teams = team
        self.rank_score = 1000 if rank_score is None else rank_score
        if last_results is not None:
            self.last_results = last_results
            self.rank_position = rank_position
        else:
            self.last_results = 1
            self.rank_position = None

    def add_result(self, is_winner: bool):
        """update last_results attribute"""
        sqlite_max_integer = 2**63
        result = (self.last_results << 1) | (1 if is_winner is True else 0)

        self.last_results = (sqlite_max_integer -1) & result

    def add_rank_score(self, score):
        """sum score to the player rank_score"""
        self.rank_score += score

        return self.rank_score

    def get_last_results(self, length):
        """return an array of last match result of the player"""

        results_count = self.last_results.bit_length() - 1
        max_results = length if results_count > length else results_count

        return [ self.last_results & (1 << i) != 0 for i in range(max_results)][::-1]

    def toJSON(self, show_last_results=False):
        """serialize Player class"""
        return {
            "id": self.id,
            "name": " ".join(filter(None, [self.name, self.surname])),
            "team": self.team,
            "score": self.rank_score,
            "last_results": None if show_last_results is False else self.get_last_results(5),
            "rank_position": self.rank_position
        }
