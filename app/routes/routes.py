from flask import Blueprint

from app.extensions.limiter import limiter

main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)
ping: Blueprint = Blueprint("ping", __name__)
testing_route: Blueprint = Blueprint("testing", __name__)

@main_route.route("/")
@limiter.exempt
def index():
    from flask import render_template

    return render_template("index.html")  # type: ignore


@get_data.post("/submit-confession")
def get_confession():
    from app.controller.get_data import get_data_web

    return get_data_web.get_data()  # type: ignore


@ping.route("/ping")
@limiter.exempt
def ping_route():
    return {"success": True}

@testing_route.post("/testing")
@limiter.exempt
def test():
    from flask import request

    print(request.get_json() or "fdsdfs", flush=True)
    return {"success": True}