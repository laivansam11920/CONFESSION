from flask import Blueprint, render_template

from app.extensions.limiter import limiter
from app.controller.get_data import get_data_web

main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)

@main_route.route("/")
@limiter.limit("10/day")
def index():
    return render_template("index.html")

@get_data.post("/submit-confession")
def get_confession():
    return get_data_web.get_data()

