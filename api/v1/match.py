"""Match router"""
from flask import Blueprint, jsonify, request

from repositories.sqlite_repo import SQLiteRepository
from services.game_service import GameService

from models.player import Teams
from models.match import Match

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

        data = request.json
        data.get("red_result")

        player_scores = game_service.game_end(
            Match(match_id, repo.get_players_by_game(match_id)),
            data.get("red_result"), data.get("blue_result")
        )

        return jsonify({
            "player_scores": player_scores
        })

    return match_bp
