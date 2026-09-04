from redis import Redis
from configs import Config

__all__ = ["r"]

r = Redis.from_url(Config.REDIS_URL, socket_timeout=5.0, socket_connect_timeout=5.0)
