"""Player router"""
from flask import Blueprint, jsonify, request
from repositories.sqlite_repo import SQLiteRepository

def players(webservice_name, repo: SQLiteRepository):
    """API per le funzionalità dei players"""

    player_bp = Blueprint('player_bp', webservice_name, url_prefix="/players")

    @player_bp.route("/")
    def get_all_players():
        """list of users"""
        query = request.args.get('query', "")

        players_response = sorted([ player.toJSON(show_last_results=True)
            for player in repo.get_players(query) ],
                key=lambda player: player["score"], reverse=True)
        return jsonify(players=players_response)

    @player_bp.route("/<player_id>", methods=['GET'])
    def get_player(player_id):
        """player details"""
        player = repo.get_player(player_id, None)

        player_matches = repo.get_match_by_player(player_id)
        return jsonify(
            player=player.toJSON(show_last_results=True),
            match_count = len(player_matches),
            matches=[ {
                "id": match.game_id,
                "state": match.state,
                "final_result": match.final_result,
                "expected_score": match.expected_score,
                "player_details": {
                    "team": match.player_details["team"],
                    "initial_score": match.player_details["initial_score"],
                    "earned_score": match.player_details["earned_score"],
                    "date": match.player_details["date"]
                }
            } for match in player_matches]
        )

    return player_bp
