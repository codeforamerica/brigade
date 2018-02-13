import os

from flask import Blueprint, Flask, render_template
from flask_webpack import Webpack
from filters import filters
from sitemap import sitemap_blueprint

brigade = Blueprint('brigade', __name__)


def create_app():
    app = Flask(__name__, static_folder='build/public/', static_url_path='/assets')
    app.config['SECRET_KEY'] = 'sekrit!'

    app.config['WEBPACK_MANIFEST_PATH'] = os.path.abspath('./brigade/build/manifest.json')
    webpack = Webpack()
    webpack.init_app(app)

    if 'SERVER_NAME' in os.environ:
        app.config['SERVER_NAME'] = os.environ['SERVER_NAME']
    if 'SITEMAP_URL_SCHEME' in os.environ:
        app.config['SITEMAP_URL_SCHEME'] = os.environ['SITEMAP_URL_SCHEME']

    app.register_blueprint(brigade)
    app.register_blueprint(filters)
    app.register_blueprint(sitemap_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app


from . import views # noqa:E402
