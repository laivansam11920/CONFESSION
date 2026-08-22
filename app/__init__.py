from flask import Flask
from app.extensions.limiter import limiter
from app.routes import register_blueprints

def create_app():

    app = Flask(__name__)
    limiter.init_app(app)
    register_blueprints(app)
    return app

