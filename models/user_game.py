"""user game model"""
from models.base_model import BaseModel

class UserGame(BaseModel):
    """UserGame Class"""
    def __init__(self, user_id, game_id, team, rank_score):
        super().__init__('user_games')

        self.user_id = user_id
        self.game_id = game_id
        self.team = team
        self.rank_score = rank_score
