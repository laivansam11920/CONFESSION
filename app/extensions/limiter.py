from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

__all__ = ["limiter"]

limiter = Limiter(
    get_remote_address,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://",
)
