"""API Routes"""
from flask import Blueprint
from repositories.sqlite_repo import SQLiteRepository

# from services.http_web_service import WEBSERVICE_NAME
from .users import users
from .players import players

def init(webservice_name, repo: SQLiteRepository):
    route = Blueprint('v1_prefix', webservice_name, url_prefix="/api/v1")
    route.register_blueprint(users(webservice_name))
    route.register_blueprint(players(webservice_name, repo))

    return route
