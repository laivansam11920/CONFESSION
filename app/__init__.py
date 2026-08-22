from flask import Flask
from app.extensions.limiter import limiter
from app.routes import register_blueprints


def create_app():

    app = Flask(__name__)
    limiter.init_app(app)
    app.secret_key = "1111111"
    register_blueprints(app)
    return app
