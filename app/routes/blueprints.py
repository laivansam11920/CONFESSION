from flask import Flask
from .routes import *


def register_blueprints(app: Flask):
    app.register_blueprint(main_route)
    app.register_blueprint(get_data)
    app.register_blueprint(test)