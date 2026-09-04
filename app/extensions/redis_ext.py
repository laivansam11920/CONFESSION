from redis import Redis
from configs import Config

r = Redis.from_url(Config.REDIS_URL)

