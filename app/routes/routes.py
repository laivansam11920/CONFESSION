from flask import Blueprint
from app.extensions.limiter import limiter

main_route: Blueprint = Blueprint("main_route", __name__)


@main_route.route("/")
@limiter.limit("10/day")
def index():
    return "hello"
