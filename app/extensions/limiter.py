from flask_limiter import Limiter
from app.utils.get_client_ip import get_client_ip

limiter = Limiter(
    key_func=get_client_ip,
    default_limits=["10 per day", "3 per hour"],
    storage_uri="memory://",
)
__all__ = ["limiter"]
