"""user model"""
from models.base_model import BaseModel

class User(BaseModel):
    """User Class"""
    def __init__(self, _id, name, surname):
        super().__init__('users')

        self.id = _id
        self.name = name
        self.surname = surname
