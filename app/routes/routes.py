from flask import Blueprint, render_template, request

from app.extensions.limiter import limiter

main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)


@main_route.route("/")
@limiter.limit("10/day")
def index():
    return render_template("index.html")


@get_data.post("/submit-confession")
def get_confession():
    from app.controller.get_data import get_data_web

    return get_data_web.get_data()


@main_route.before_request
def get_info_user():
    user_ip = request.remote_addr
