from flask import Blueprint

home_bp = Blueprint("home", __name__)


@home_bp.get("/")
def home():
    return "Hello World"
