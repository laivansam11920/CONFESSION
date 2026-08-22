from flask import Flask
from flask_babel import Babel

from app.extensions.limiter import limiter
from app.routes import register_blueprints
from .utils.change_lang import get_locale
from configs import Config


def create_app():

    app = Flask(__name__)
    babel = Babel()
    limiter.init_app(app)
    app.secret_key = "1111111"
    app.config.from_object(Config)
    babel.init_app(app, locale_selector=get_locale)
    register_blueprints(app)
    return app
