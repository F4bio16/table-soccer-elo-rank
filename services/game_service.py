"""user service"""
from models.game import GameState
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

            for player in players:
                self.repo.create_usergame(game_id, player.id, player.team)

            return match
        except EloException:
            pass
        except Exception:
            if game_id is not None:
                self.repo.delete_game(game_id)

        return None

    def game_end(self, match: Match, team_red_score: int, team_blue_score: int):
        """
            termina il game:
            - aggiorniamo lo stato sul DB
            - calcoliamo l'expected score delle due squadre
            - calcoliamo il nuovo rank dei giocatori
            - aggiorniamo il rank dei giocatori
        """

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

        winner = Teams.RED.value if team_red_score > team_blue_score else Teams.BLUE.value
        players = self.repo.get_players_by_game(match.game_id)

        self.repo.update_game(
            match.game_id,
            GameState.END.value,
            f"{team_red_score}:{team_blue_score}"
        )

        total_rank_scores = {Teams.RED.value: 0, Teams.BLUE.value: 0}
        for player in players:
            total_rank_scores[player.team] += player.rank_score

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

        for player in players:
            player.add_result(True if (winner == player.team) else False)

            match_point = match.opponents[player.team]["match_points"]
            player.add_rank_score(match_point)
            self.repo.update_user_rank(player.id, player.rank_score, player.last_results)
            self.repo.close_user_game(match.game_id, player.id, match_point)

        return players
