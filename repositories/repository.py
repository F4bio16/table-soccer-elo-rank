"""Repository interface"""
from abc import ABC, abstractmethod

from models.player import Player, Teams
from models.match import Match

class Repository(ABC):
    """Repository Abstract Class"""

    @abstractmethod
    def connect(self):
        """method for connect to the repository"""

    @abstractmethod
    def create_user(self, name: str, surname: str):
        """method for create user and initialize his rank"""

    @abstractmethod
    def create_game(self):
        """method for create game record and return game_id"""

    @abstractmethod
    def create_usergame(self, game_id: int, player_id: int, player_team):
        """method for assign user to the game"""

    @abstractmethod
    def delete_game(self, game_id: int):
        """method for delete game by game_id"""

    @abstractmethod
    def update_game(self, game_id: int, state, final_result):
        """method for update game record"""

    @abstractmethod
    def game_set_expected_scores(self, match: Match):
        """method for set expected_scores of a match"""

    @abstractmethod
    def get_player(self, user_id: int, team: Teams) -> Player:
        """return player by user_id"""

    @abstractmethod
    def get_players_by_game(self, game_id: int) -> list[Player]:
        """return list of players of a game"""

    @abstractmethod
    def update_user_rank(self, user_id: int, points: int, last_results: int(8)):
        """Update user rank"""

    @abstractmethod
    def get_match(self, match_id: int):
        """return match by ID"""

    @abstractmethod
    def get_last_matches(self, limit: int):
        """return list of recent match"""
