"""PlayerScore model"""
from models.player import Player

class PlayerScore(Player):
    """PlayerScore class"""
    def __init__(self, player, user_game):
        super().__init__(player.id, player.name, player.surname,
          player.team, player.rank_score, player.last_results)
        self.initial_score = user_game.initial_score
        self.earned_score = user_game.earned_score

    def toJSON(self):
        """serialize Player class"""
        return {
            "id": self.id,
            "name": " ".join(filter(None, [self.name, self.surname])),
            "team": self.team,
            "score": self.rank_score,
            "initial_score": self.initial_score,
            "earned_score": self.earned_score
        }
