"""game model"""
from enum import Enum
from models.base_model import BaseModel

class GameState(Enum):
    """enumeration for Game.state attribute values"""
    INITIAL = '__initial__'
    PROGRESS = '__progress__'
    SUSPEND = '__suspend__'
    END = '__end__'
    DELETED = '__deleted__'

class Game(BaseModel):
    """Game Class"""
    def __init__(self, _id, state, final_result):
        super().__init__('games')

        self.id = _id
        self.state = state
        self.final_result = final_result
