"""Modulo per l'avvio e gestione del Web server HTTP"""
from flask import Flask # , render_template
from repositories.sqlite_repo import SQLiteRepository
from services.game_service import GameService

from api.v1 import v1_route

WEBSERVICE_NAME = "elo_ranking"

class HttpWebService:
    """HttpWebService class"""
    def __init__(self, repo: SQLiteRepository, game_service: GameService):
        self.server = Flask(WEBSERVICE_NAME)
        self.sqlite_repository = repo
        self.game_service = game_service

        self.server.register_blueprint(
            v1_route.init(WEBSERVICE_NAME, self.sqlite_repository, self.game_service)
        )

    def start(self, listening_port):
        """staring WebServer to listening_port"""
        self.server.run(debug=True, port=listening_port)
