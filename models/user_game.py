"""user game model"""
from models.base_model import BaseModel
from models.player import Teams, Player
from models.match import Match

class UserGame(BaseModel):
    """UserGame Class"""
    def __init__(self, game_id: int, user_id: int, team: Teams, initial_score: int, earned_score: int, created_at: str):
        super().__init__('user_games')

        self.user_id = user_id
        self.game_id = game_id
        self.team = team
        self.initial_score = initial_score
        self.earned_score = earned_score
        self.created_at = created_at

    def set_earned_score(self, earned_score):
        self.earned_score = earned_score

    @staticmethod
    def get_instance(match: Match, player: Player):
        return UserGame(match.game_id, player.id, player.team, player.rank_score, None, None)
