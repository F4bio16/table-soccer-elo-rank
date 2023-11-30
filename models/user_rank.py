"""user rank model"""
from models.base_model import BaseModel

class UserRank(BaseModel):
    """UserRank Class"""
    def __init__(self, user_id, points, created_at, updated_at, last_results):
        super().__init__('user_ranks')
        self.user_id = user_id
        self.points = points
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_results = last_results
