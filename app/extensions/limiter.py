from flask_limiter import Limiter
from app.utils.get_client_ip import get_client_ip

__all__ = ["limiter"]

limiter = Limiter(
    key_func=get_client_ip,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://",
)
