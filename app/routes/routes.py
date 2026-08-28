from flask import Blueprint, render_template, request

from app.extensions.limiter import limiter

main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)

test: Blueprint = Blueprint("test", __name__)

@main_route.route("/")
@limiter.limit("10/day")
def index():
    return render_template("index.html")  # type: ignore


@get_data.post("/submit-confession")
@limiter.limit("10/day")
def get_confession():
    from app.controller.get_data import get_data_web

    return get_data_web.get_data()  # type: ignore

@test.route('/debug-ip')
def debug_ip():
    return {
        "remote_addr": request.remote_addr,
        "x_forwarded_for": request.headers.get('X-Forwarded-For')
    }