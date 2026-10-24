from flask import Blueprint

from app.extensions.limiter import limiter


__all__ = ["ping"]

ping: Blueprint = Blueprint("ping", __name__)

@ping.route("/ping")
@limiter.exempt
def ping_route():
    return {"success": True}
