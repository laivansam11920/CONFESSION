from flask import Blueprint

from app.extensions.limiter import limiter
from app.extensions.crfs import crfs
from app.utils.logger import console

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
    try:
        from app.controller.get_data import get_data_web

        return get_data_web.get_data()  # type: ignore
    except Exception as e:
        console.error(e)
        return {"msg": "this feature is not available"}

@get_data.post("/submit-confession-form")
@crfs.exempt
def get_confession_form():
    try:
        from app.controller.get_data import get_data_google

        return get_data_google.get_data()  # type: ignore
    except Exception as e:
        console.error(e)
        return {"msg": "this feature is not available"}


@ping.route("/ping")
@limiter.exempt
def ping_route():
    return {"success": True}
