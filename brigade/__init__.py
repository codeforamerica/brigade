from flask import Blueprint, Flask
from filters import filters
from flask.ext.github import GitHub

brigade = Blueprint('brigade', __name__)
github = GitHub()

def create_app(environ):
    app = Flask(__name__, static_folder='static', static_url_path='/brigade/static')
    app.secret_key = "sangria wreath"
    app.config['BRIGADE_SIGNUP_SECRET'] = environ['BRIGADE_SIGNUP_SECRET']
    app.config['GITHUB_CLIENT_ID'] = environ['GITHUB_CLIENT_ID']
    app.config['GITHUB_CLIENT_SECRET'] = environ['GITHUB_CLIENT_SECRET']

    # github.app = app
    github.init_app(app)

    app.register_blueprint(brigade)
    app.register_blueprint(filters)
    return app

from . import views
