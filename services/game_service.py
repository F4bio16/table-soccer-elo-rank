"""user service"""
from models.game import GameState
from models.user_game import UserGame
from models.player import Player, Teams
from models.match import Match

from services.rank_service import RankService

from config.exceptions import EloException

class GameService:
    """GameService Class"""
    def __init__(self, repo, rank_service: RankService):
        self.repo = repo
        self.rank_service: RankService = rank_service

    def game_start(self, players: list[Player]):
        """crea il nuovo game assegnandogli gli users"""
        game_id = None
        try:
            game_id = self.repo.create_game()

            match = Match(game_id, players)
            match.get_team_points(Teams.RED.value)

            match.set_expected_score(Teams.RED.value,
                self.rank_service.calculate_expected_score(
                    match.get_team_points(Teams.RED.value),
                    match.get_team_points(Teams.BLUE.value)
            ))

            match.set_expected_score(Teams.BLUE.value,
                self.rank_service.calculate_expected_score(
                    match.get_team_points(Teams.BLUE.value),
                    match.get_team_points(Teams.RED.value)
            ))

            # save expected score of the match
            self.repo.game_set_expected_scores(match)

            for player in players:
                self.repo.create_usergame(UserGame.get_instance(match, player))

            return match
        except EloException as e:
            print(e)
            pass
        except Exception as e:
            print(e)
            if game_id is not None:
                self.repo.delete_game(game_id)
        finally:
            print

        return None

    def game_end(self, match: Match, team_red_score: int, team_blue_score: int):
        """
            termina il game:
            - aggiorniamo lo stato sul DB
            - calcoliamo l'expected score delle due squadre
            - calcoliamo il nuovo rank dei giocatori
            - aggiorniamo il rank dei giocatori
        """

        winner = Teams.RED.value if team_red_score > team_blue_score else Teams.BLUE.value
        players = self.repo.get_players_by_game(match.game_id)

        self.repo.update_game(
            match.game_id,
            GameState.END.value,
            f"{team_red_score}:{team_blue_score}"
        )

        match.finish((team_red_score, team_blue_score))

        match.set_match_points(
            (
                self.rank_service.calculate_ranking_points(
                    self.rank_service.get_match_score(
                        team_red_score, match.get_winner_opponent()["match_score"]
                    ),
                    match.get_expected_score(Teams.RED.value)
                ),
                self.rank_service.calculate_ranking_points(
                    self.rank_service.get_match_score(
                        team_blue_score, match.get_winner_opponent()["match_score"]
                    ),
                    match.get_expected_score(Teams.BLUE.value)
                )
            )
        )

        for el in players:
            player = el[0]
            player.add_result(winner == player.team)

            match_point = match.opponents[player.team]["match_points"]

            user_game = UserGame.get_instance(match, player)
            user_game.set_earned_score(match_point)

            player.add_rank_score(match_point)

            self.repo.update_user_rank(player.id, player.rank_score, player.last_results)
            self.repo.update_user_game(user_game)

        return players
