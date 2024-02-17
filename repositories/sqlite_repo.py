"""Repository implementation for SQLite database"""
import sqlite3
from time import time

from models.game import GameState
from models.user_game import UserGame
from models.player import Player, Teams
from models.match import Match

from repositories.repository import Repository

class SQLiteRepository(Repository):
    """SQLiteRepository Class extends Repository abstract Class"""
    def __init__(self, configs):
        self.is_connected = False
        self.connection = None
        self.configs = configs

    def connect(self):
        if self.is_connected is True:
            print("Connecting to datasource: A connection alread exists")
        else:
            print("Connecting to datasource")

        self.connection = sqlite3.connect(self.configs["DB_NAME"], check_same_thread=False)
        self.is_connected = True

    def create_user(self, name: str, surname: str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (name, surname) VALUES (?, ?)", (name, surname))
        self.connection.commit()

        return cursor.lastrowid

    def create_game(self):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO games ( state ) VALUES (?)", (GameState.INITIAL.value,))
        self.connection.commit()

        return cursor.lastrowid

    def create_usergame(self, user_game: UserGame):
        """Crea un nuovo user_game"""

        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO user_games
            (game_id, user_id, team, initial_score, earned_score)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_game.game_id,
                user_game.user_id,
                user_game.team,
                user_game.initial_score,
                user_game.earned_score
            )
        )
        self.connection.commit()

    def update_user_game(self, user_game: UserGame):
        """Aggiorno attributi di user_game"""

        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE user_games SET team = ?, initial_score = ?, earned_score = ?
            WHERE game_id = ? AND user_id = ?
            """,
            (
                user_game.team,
                user_game.initial_score,
                user_game.earned_score,
                user_game.game_id,
                user_game.user_id
            ))
        self.connection.commit()

    def delete_game(self, game_id: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM user_games WHERE game_id = ?", (game_id,))
        cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.connection.commit()

    def update_game(self, game_id: int, state, final_result,
        red_humiliated: bool, blue_humiliated: bool):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE games
            SET
                state = ?,
                final_result = ?,
                end_at = ?,
                args = json_set(args, '$.red_humiliated', ?, '$.blue_humiliated', ?)
            WHERE id = ?
        """,
        (state, final_result, time(), red_humiliated, blue_humiliated, game_id))

        self.connection.commit()

    def game_set_expected_scores(self, match: Match):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE games SET expected_scores = ? WHERE id = ?", (
            f"""{match.get_expected_score(Teams.RED.value)}|{
            match.get_expected_score(Teams.BLUE.value)}""",
            match.game_id)
        )
        self.connection.commit()

    def update_game_state(self, game_id: int, state: GameState):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE games SET state = ? WHERE id = ?", (state.value, game_id)
        )

        self.connection.commit()

    def get_players(self, query: str) -> list[Player]:
        """Restituisce la lista di giocatori (Player)"""

        cursor = self.connection.cursor()
        cursor.execute("""
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
        for result in cursor.fetchall():
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
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT users.name, users.surname, user_ranks.points, user_ranks.last_results
            FROM users
            LEFT JOIN user_ranks ON (users.id = user_ranks.user_id)
            WHERE users.id = ?
            """,
            (user_id,)
        )

        result = cursor.fetchone()
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

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT
                user_games.user_id,
                users.name,
                users.surname,
                user_games.team,
                ur.points,
                ur.last_results,
                (SELECT COUNT(DISTINCT points) from user_ranks WHERE points > ur.points) +1,
                user_games.initial_score,
                user_games.earned_score,
                user_games.created_at
            FROM user_games
            LEFT JOIN users ON (user_games.user_id = users.id)
            LEFT JOIN user_ranks ur ON (user_games.user_id = ur.user_id)
            WHERE user_games.game_id = ?
            """,
            (game_id,)
        )

        players_list = []
        for result in cursor.fetchall():
            player = Player(
                result[0],
                result[1],
                result[2],
                result[3],
                result[4],
                result[5]
            )
            user_game = UserGame(game_id, result[0], result[3], result[7], result[8], result[9])
            players_list.append([player, user_game])

        return players_list

    def update_user_rank(self, user_id: int, points: int, last_results: int(8)):
        """Aggiorna il rank di un utente"""

        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM user_ranks WHERE user_id = ?", (user_id,))

        if len(cursor.fetchall()) > 0:
            cursor.execute("""
                UPDATE user_ranks
                SET points = ?, last_results = ?, updated_at = ?
                WHERE user_id = ?
                """, (points, last_results, time(), user_id))
        else:
            cursor.execute("""
                INSERT INTO user_ranks (user_id, points, created_at, updated_at, last_results)
                VALUES (?, ?, ?, ?, ?)
                """, (user_id, points, time(), time(), last_results))
        self.connection.commit()

    def get_match(self, match_id: int):
        """Get match by ID"""

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, state, final_result, expected_scores
            FROM games
            where id = ?
            """,
            (match_id,))

        result = cursor.fetchone()
        return Match.get_instance(
            result[0],
            result[1],
            result[2],
            result[3]
        )

    def get_last_matches(self, limit: int):
        """Recupera gli ultimi match giocati"""

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT
                games.id, games.state, games.final_result,
                games.expected_scores, games.created_at, games.end_at, games.args
            FROM games
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        matches = []
        for result in cursor.fetchall():
            curr_match = Match.get_instance(
                result[0],
                result[1],
                result[2],
                result[3]
            )
            curr_match.set_durations(result[4], result[5])
            curr_match.set_args(result[6])

            matches.append(curr_match)
        return matches

    def get_match_by_player(self, user_id: int):
        """Get match by ID"""

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT games.id, games.state, games.final_result, games.expected_scores,
                user_games.team, user_games.initial_score, user_games.earned_score,
                user_games.created_at
            FROM games
            LEFT JOIN user_games ON (user_games.game_id = games.id)
            WHERE user_games.user_id = ?
            ORDER BY user_games.created_at DESC
            """,
            (user_id,))

        matches = []
        for result in cursor.fetchall():
            curr_match = Match.get_instance(
                result[0],
                result[1],
                result[2],
                result[3]
            )
            curr_match.player_details = dict(
                team=result[4],
                initial_score=result[5],
                earned_score=result[6],
                date=result[7]
            )

            matches.append(curr_match)

        return matches

    def get_last_match_by_state(self, status: GameState):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT games.id, games.state, games.final_result, games.expected_scores
            FROM games
            WHERE state = ?
            ORDER BY end_at DESC
            LIMIT 1
            """,
            (status.value, )
        )

        result = cursor.fetchone()
        if result is None:
            return None

        return Match.get_instance(
            result[0],
            result[1],
            result[2],
            result[3]
        )
