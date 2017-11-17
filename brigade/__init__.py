from flask import Blueprint, Flask
from filters import filters

brigade = Blueprint('brigade', __name__)


def create_app():
    app = Flask(__name__, static_url_path='/brigade/static')
    app.config['SECRET_KEY'] = 'sekrit!'

    app.register_blueprint(brigade)
    app.register_blueprint(filters)
    return app


from . import views # noqa:E402
