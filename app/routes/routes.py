from flask import Blueprint

from app.extensions.limiter import limiter

main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)
ping: Blueprint = Blueprint("ping", __name__)

@main_route.route("/")
@limiter.limit("10/day")
def index():
    from flask import render_template

    return render_template("index.html")  # type: ignore


@get_data.post("/submit-confession")
@limiter.limit("10/day")
def get_confession():
    from app.controller.get_data import get_data_web

    return get_data_web.get_data()  # type: ignore

@ping.route("/ping")
def ping():
    print("1", flush=True)
    return {"success": True}