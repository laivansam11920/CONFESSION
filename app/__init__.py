from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():

    app = Flask(__name__)

    limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"], storage_uri="memory://",)
    limiter.init_app(app)


    @app.route("/")
    @limiter.limit("10/day")
    def index():
        return "hello"

    return app
