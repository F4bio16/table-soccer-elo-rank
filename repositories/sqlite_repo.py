"""Repository implementation for SQLite database"""
import sqlite3
from time import time

from models.game import GameState
from models.player import Player, Teams
from models.match import Match

from repositories.repository import Repository

class SQLiteRepository(Repository):
    """SQLiteRepository Class extends Repository abstract Class"""
    def __init__(self, configs):
        self.is_connected = False
        self.connection = None
        self.cursor = None

        self.configs = configs

    def connect(self):
        if self.is_connected is True:
            print("Connecting to datasource: A connection alread exists")
        else:
            print("Connecting to datasource")

        self.connection = sqlite3.connect(self.configs["DB_NAME"], check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.is_connected = True

    def create_user(self, name: str, surname: str):
        self.cursor.execute("INSERT INTO users (name, surname) VALUES (?, ?)", (name, surname))
        self.connection.commit()

        return self.cursor.lastrowid

    def create_game(self):
        self.cursor.execute("INSERT INTO games ( state ) VALUES (?)", (GameState.INITIAL.value,))
        self.connection.commit()

        return self.cursor.lastrowid

    def create_usergame(self, game_id: int, player_id: int, player_team: Teams):
        self.cursor.execute("INSERT INTO user_games (user_id, game_id, team) VALUES (?, ?, ?)",
            (player_id, game_id, player_team))
        self.connection.commit()

    def delete_game(self, game_id: int):
        self.cursor.execute("DELETE FROM user_games WHERE game_id = ?", (game_id,))
        self.cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.connection.commit()

    def update_game(self, game_id: int, state, final_result):
        self.cursor.execute("UPDATE games SET state = ?, final_result = ? WHERE id = ?",
            (state, final_result, game_id))
        self.connection.commit()

    def game_set_expected_scores(self, match: Match):
        self.cursor.execute(
            "UPDATE games SET expected_scores = ? WHERE id = ?", (
            f"""{match.get_expected_score(Teams.RED.value)}|{
            match.get_expected_score(Teams.BLUE.value)}""",
            match.game_id)
        )
        self.connection.commit()

    def get_players(self, query: str) -> list[Player]:
        """Restituisce la lista di giocatori (Player)"""
        self.cursor.execute("""
            SELECT
            users.id,
            users.name,
            users.surname,
            ur.points,
            ur.last_results,
            (SELECT COUNT(DISTINCT points) from user_ranks WHERE points > ur.points AND last_results != 1) +1
            FROM users
            LEFT JOIN user_ranks ur ON (users.id = ur.user_id)
            WHERE name LIKE ? OR surname LIKE ?
            """,
            ("%"+query+"%","%"+query+"%")
        )

        players_list = []
        for result in self.cursor.fetchall():
            players_list.append(Player(
                result[0],
                result[1],
                result[2],
                None,
                result[3],
                result[4],
                result[5]
            ))

        return players_list

    def get_player(self, user_id: int, team: Teams) -> Player:
        self.cursor.execute("""
            SELECT users.name, users.surname, user_ranks.points, user_ranks.last_results
            FROM users
            LEFT JOIN user_ranks ON (users.id = user_ranks.user_id)
            WHERE users.id = ?
            """,
            (user_id,)
        )

        result = self.cursor.fetchone()
        return Player(
            user_id,
            result[0],
            result[1],
            team,
            result[2],
            result[3]
        )

    def get_players_by_game(self, game_id: int) -> list[Player]:
        """Restituisce la lista di giocatori (Player) di un match"""
        self.cursor.execute("""
            SELECT
                user_games.user_id,
                users.name,
                users.surname,
                user_games.team,
                ur.points,
                ur.last_results,
                (SELECT COUNT(DISTINCT points) from user_ranks WHERE points > ur.points) +1
            FROM user_games
            LEFT JOIN users ON (user_games.user_id = users.id)
            LEFT JOIN user_ranks ur ON (user_games.user_id = ur.user_id)
            WHERE user_games.game_id = ?
            """,
            (game_id,)
        )

        players_list = []
        for result in self.cursor.fetchall():
            players_list.append(Player(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4],
                result[5]
            ))

        return players_list

    def update_user_rank(self, user_id: int, points: int, last_results: int(8)):
        """Aggiorna il rank di un utente"""
        self.cursor.execute("SELECT user_id FROM user_ranks WHERE user_id = ?", (user_id,))

        if len(self.cursor.fetchall()) > 0:
            self.cursor.execute("""
                UPDATE user_ranks
                SET points = ?, last_results = ?, updated_at = ?
                WHERE user_id = ?
                """, (points, last_results, time(), user_id))
        else:
            self.cursor.execute("""
                INSERT INTO user_ranks (user_id, points, created_at, updated_at, last_results)
                VALUES (?, ?, ?, ?, ?)
                """, (user_id, points, time(), time(), last_results))
        self.connection.commit()

    def close_user_game(self, game_id: int, user_id: int, rank_score: int):
        """Salva i punti vinti nel game"""

        self.cursor.execute("""
                UPDATE user_games SET rank_score = ? WHERE game_id = ? AND user_id = ?
            """,
            (rank_score, game_id, user_id)
        )
        self.connection.commit()

    def get_match(self, match_id: int):
        """Get match by ID"""
        self.cursor.execute("""
            SELECT id, state, final_result, expected_scores
            FROM games
            where id = ?
            """,
            (match_id,))

        result = self.cursor.fetchone()
        return Match.get_instance(
            result[0],
            result[1],
            result[2],
            result[3]
        )

    def get_last_matches(self, limit: int):
        """Recupera gli ultimi 10 match giocati"""

        self.cursor.execute("""
            SELECT games.id, games.state, games.final_result, games.expected_scores
            FROM games
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        matches = []
        for result in self.cursor.fetchall():
            matches.append(
                Match.get_instance(
                    result[0],
                    result[1],
                    result[2],
                    result[3]
                ))
        return matches
