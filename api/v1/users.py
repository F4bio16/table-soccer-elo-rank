"""User router"""
from flask import Blueprint

def users(webservice_name):
    user_bp = Blueprint('user_bp', webservice_name, url_prefix="/users")

    @user_bp.route("/")
    def index():
        """index"""
        return "Hello world"

    return user_bp
