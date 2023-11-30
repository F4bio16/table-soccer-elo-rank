"""BaseModel interface"""
from abc import ABC

class BaseModel(ABC):
    """Interface for all models"""
    def __init__(self, tablename):
        self.__tablename__ = tablename
