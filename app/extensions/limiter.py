from flask_limiter import Limiter

from app.utils.get_client_tracking import get_client_tracking
from configs import Config

limiter = Limiter(
    key_func=get_client_tracking,
    default_limits=["10 per 10 minutes"],
    storage_uri=Config.REDIS_URL or "memory://",
)
__all__ = ["limiter"]
