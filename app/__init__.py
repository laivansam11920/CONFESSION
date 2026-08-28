from flask import Flask
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect

from app.extensions.limiter import limiter
from app.routes import register_blueprints
from .utils.change_lang import get_locale
from configs import Config

from werkzeug.middleware.proxy_fix import ProxyFix


def create_app() -> Flask:

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_proto=1, x_host=1)
    babel = Babel()
    limiter.init_app(app)
    app.config.from_object(Config)
    CSRFProtect(app)
    babel.init_app(app, locale_selector=get_locale)
    register_blueprints(app)

    return app
