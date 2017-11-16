from flask import Blueprint, Flask, url_for
from flask_sitemap import Sitemap
from filters import filters
from sitemap import sitemap_blueprint

brigade = Blueprint('brigade', __name__, static_folder='static')

def create_app():
    app = Flask(__name__, static_url_path='/brigade/static')
    app.config['SECRET_KEY'] = 'sekrit!'

    app.register_blueprint(brigade)
    app.register_blueprint(filters)
    app.register_blueprint(sitemap_blueprint)
    return app

from . import views
