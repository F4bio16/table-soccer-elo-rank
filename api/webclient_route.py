from flask import Blueprint, render_template
from repositories.sqlite_repo import SQLiteRepository

def init(webservice_name, repo: SQLiteRepository):
    blueprint = Blueprint('webclient', webservice_name,
        url_prefix="", template_folder='./web-client/')

    @blueprint.route('/')
    @blueprint.route('/index')
    @blueprint.route('/index.html')
    def index():
        return render_template('index.html')

    @blueprint.route('/players')
    def player_list():
        return render_template('players.html')

    @blueprint.route('/players/<player_id>')
    def player_details(player_id):
        try:
            player = repo.get_player(player_id, None)
            if player is None:
                return 'Not found', 404

            return render_template('player_details.html', player=player)
        except:
            return 'Not found', 404

    @blueprint.route('/matches')
    def matches_list():
        return render_template('matches.html')

    return blueprint
