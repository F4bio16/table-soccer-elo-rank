"""API Routes"""
from flask import Blueprint
from repositories.sqlite_repo import SQLiteRepository
from services.game_service import GameService

# from services.http_web_service import WEBSERVICE_NAME
from .users import users
from .players import players
from .match import matches

def init(webservice_name, repo: SQLiteRepository, game_service: GameService):
    route = Blueprint('v1_prefix', webservice_name, url_prefix="/api/v1")
    route.register_blueprint(users(webservice_name))
    route.register_blueprint(players(webservice_name, repo))
    route.register_blueprint(matches(webservice_name, repo, game_service))

    return route
