from flask import Blueprint
from app.extensions.limiter import limiter

__all__ = ["moderation"]

moderation: Blueprint = Blueprint("moderation", __name__)


@moderation.get("/moderation")
@limiter.exempt
def moderation_route():
    from app.controller.moderation import moderation_ctl

    return moderation_ctl()


@moderation.post("/api-moderation")
@limiter.exempt
def moderation_api():
    from app.controller.moderation import moderation_api_ctl

    return moderation_api_ctl()
