"""Match router"""
from flask import Blueprint, jsonify, request

from repositories.sqlite_repo import SQLiteRepository
from services.game_service import GameService

from models.player import Teams
from models.match import Match
from models.game import GameState

def matches(webservice_name, repo: SQLiteRepository, game_service: GameService):
    match_bp = Blueprint('match_bp', webservice_name, url_prefix="/matches")

    @match_bp.route("/start", methods=['POST'])
    def start_match():
        """start new match"""
        data = request.json

        red_team_player_ids = data.get('red_team')
        blue_team_player_ids = data.get('blue_team')

        players = []

        for player_id in red_team_player_ids:
            players.append(repo.get_player(player_id, Teams.RED.value))

        for player_id in blue_team_player_ids:
            players.append(repo.get_player(player_id, Teams.BLUE.value))

        match = game_service.game_start(players)

        return jsonify({"game_id": match.game_id,
            "expected_scores": {
                "red_wins": match.get_expected_score(Teams.RED.value),
                "blue_wins": match.get_expected_score(Teams.BLUE.value)
            }
        })

    @match_bp.route("/<match_id>/complete", methods=['POST'])
    def complete_match(match_id):
        """terminate match and set result"""

        print(f"called complete_match api with match_id {match_id}")

        match = repo.get_match(int(match_id))
        if match.state != GameState.INITIAL.value:
            return 'Unable to close match with invalid state', 403

        data = request.json

        _players = repo.get_players_by_game(match.game_id)
        for player in _players:
            match.set_player(player, None)

        final_scores = game_service.game_end(
            match,
            data.get("red_result"), data.get("blue_result")
        )

        return jsonify({
            "player_scores": [
                { **player.toJSON(), **{ "score_delta": match.get_match_points(player.team)}}
                for player in final_scores]
        })

    @match_bp.route('/', methods=['GET'])
    def get_matches():
        """Visualizzo gli ultimi match giocati"""

        limit = request.args.get('limit', default=10, type=int)
        last_matches = repo.get_last_matches(limit)

        results = []
        for match in last_matches:
            for player in repo.get_players_by_game(match.game_id):
                match.set_player(player, None)
            results.append(match)

        return jsonify({
            "matches": [{
                "id": result.game_id,
                "state": result.state,
                "red_score": int(result.final_result.split(":")[0])
                    if result.final_result is not None else None,
                "blue_score": int(result.final_result.split(":")[1])
                    if result.final_result is not None else None,
                "red_players": [player.toJSON() for player in result.opponents[Teams.RED.value]["players"]],
                "blue_players": [player.toJSON() for player in result.opponents[Teams.BLUE.value]["players"]]
            } for result in results]
        })

    return match_bp
