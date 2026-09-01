from flask import Flask, Blueprint
from .routes import *

__all__ = ["register_blueprints"]


def register_blueprints(app: Flask):

    all_routes: list[Blueprint] = [
        main_route,
        get_data,
        ping,
        testing_route,
    ]

    for route in all_routes:
        app.register_blueprint(route)
