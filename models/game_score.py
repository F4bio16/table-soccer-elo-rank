"""game score model"""
from models.base_model import BaseModel
from models.match import Match
from models.player import Player

class _GameScore(BaseModel):
    """GameScore Class"""

    def __init__(self, game_id: int, user_id: int,
        initial_score: int, earned_score: int, created_at: str):
        super().__init__('game_score')

        self.game_id = game_id
        self.user_id = user_id
        self.initial_score = initial_score
        self.earned_score = earned_score
        self.created_at = created_at

    def set_earned_score(self, earned_score):
        self.earned_score = earned_score

    @staticmethod
    def get_instance(match: Match, player: Player):
        return _GameScore(match.game_id, player.id, player.rank_score, None, None)
