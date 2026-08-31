from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions.limiter import limiter
from app.extensions.crfs import crfs
from app.extensions.babel import babel
from app.routes import register_blueprints
from .utils.change_lang import get_locale
from configs import Config


def create_app() -> Flask:

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_proto=1, x_host=1)
    app.config.from_object(Config)
    limiter.init_app(app)
    crfs.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    register_blueprints(app)

    return app
