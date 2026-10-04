from flask_limiter import Limiter

from app.utils.get_client_tracking import get_client_tracking
from app.utils.logger import console
from configs import Config

try:
    limiter = Limiter(
        key_func=get_client_tracking,
        default_limits=[Config.DEFAULT_RATE_LIMIT],
        storage_uri=Config.REDIS_URL or "memory://",
    )
except Exception as e:
    console.error(e)

__all__ = ["limiter"]
