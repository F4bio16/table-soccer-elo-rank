"""User router"""
from flask import Blueprint, jsonify
from repositories.sqlite_repo import SQLiteRepository

def players(webservice_name, repo: SQLiteRepository):
    player_bp = Blueprint('player_bp', webservice_name, url_prefix="/players")

    @player_bp.route("/")
    def get_all_players():
        """list of users"""
        all_players = repo.get_players()
        result = []
        for player in all_players:
            result.append(player.toJSON())

        return jsonify(result)

    return player_bp
