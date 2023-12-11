from flask import Blueprint, render_template

def init(webservice_name):
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

    return blueprint
