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

        return jsonify(
            sorted([ player.toJSON() for player in repo.get_players(query) ],
                key=lambda player: player["score"], reverse=True))

    return player_bp
