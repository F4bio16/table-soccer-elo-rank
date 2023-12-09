"""player model"""
from enum import Enum

from models.user import User

class Teams(Enum):
    """enumeration for Player.team values"""
    RED = '__red__'
    BLUE = '__blue__'

class Player(User):
    """Player Class extended by User"""

    def __init__(self, _id, name, surname, team: Teams, rank_score, last_results):
        super().__init__(_id=_id,name=name,surname=surname)

        self.team: Teams = team
        self.rank_score = 1000 if rank_score is None else rank_score
        self.last_results = 1 if last_results is None else last_results

    def add_result(self, is_winner: bool):
        """update last_results attribute"""
        self.last_results = (self.last_results << 1) | (1 if is_winner is True else 0)

    def add_rank_score(self, score):
        """sum score to the player rank_score"""
        self.rank_score += score

        return self.rank_score

    def toJSON(self):
        """serialize Player class"""
        return {
            "id": self.id,
            "name": " ".join(filter(None, [self.name, self.surname])),
            "team": self.team,
            "score": self.rank_score,
            "last_results": self.last_results
        }
