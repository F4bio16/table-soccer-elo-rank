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

    def delete_game(self, game_id: int):
        """
            Elimina una partita solo se:
                - è in stato "iniziale"
                - è l'ultima partita completata - ricalcolo i punteggi dei partecipanti
            negli altri casi restituisco errore
        """
        match = self.repo.get_match(game_id)

        if match.state == GameState.INITIAL.value:
            self.repo.update_game_state(game_id, GameState.DELETED)
            return True

        last_match = self.repo.get_last_match_by_state(GameState.END)
        if last_match.game_id != match.game_id:
            return False

        results = self.repo.get_players_by_game(match.game_id)
        for result in results:
            player = result[0]
            user_game = result[1]

            # reload point for users of the match
            self.repo.update_user_rank(
                player.id,
                user_game.initial_score,
                # remove last result data
                player.last_results >> 1
            )

        # change game status
        self.repo.update_game_state(game_id, GameState.DELETED)
        return True

    def game_end(
        self,
        match: Match,
        team_red_score: int,
        team_blue_score: int,
        team_red_humiliated: bool = False,
        team_blue_humiliated: bool = False):
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
            f"{team_red_score}:{team_blue_score}",
            team_red_humiliated,
            team_blue_humiliated
        )

        match.finish((team_red_score, team_blue_score))

        match.set_match_points(
            (
                self.rank_service.calculate_ranking_points(
                    self.rank_service.get_match_score(
                        team_red_score, match.get_winner_opponent()["match_score"]
                    ),
                    match.get_expected_score(Teams.RED.value),
                    dict(humiliated = team_red_humiliated, humiliating = team_blue_humiliated)
                ),
                self.rank_service.calculate_ranking_points(
                    self.rank_service.get_match_score(
                        team_blue_score, match.get_winner_opponent()["match_score"]
                    ),
                    match.get_expected_score(Teams.BLUE.value),
                    dict(humiliated = team_blue_humiliated, humiliating = team_red_humiliated)
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
