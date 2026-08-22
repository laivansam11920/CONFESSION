from flask import Flask
from .routes import *


def register_blueprints(app: Flask):
    app.register_blueprint(main_route)
