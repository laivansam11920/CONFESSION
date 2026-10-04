from redis import Redis

from app.utils.logger import console
from configs import Config

__all__ = ["r"]

try:

    r = Redis.from_url(
        Config.REDIS_URL,
        socket_timeout=5.0,
        socket_connect_timeout=5.0,
        decode_responses=True,
    )

except Exception as e:
    console.error(e)
