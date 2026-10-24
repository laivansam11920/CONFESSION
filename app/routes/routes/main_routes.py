from flask import Blueprint

from app.extensions.limiter import limiter
from configs import Config

__all__ = ["main_route"]

main_route: Blueprint = Blueprint("main_route", __name__)

if Config.CHANGE_GET_DATA_BY_WEB:

    @main_route.route("/")
    @limiter.exempt
    def index():
        from flask import render_template

        return render_template("index.html")  # type: ignore