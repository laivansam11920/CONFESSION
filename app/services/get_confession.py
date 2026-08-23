from app.base import ConfessionManager
from app.utils.logger import logger
from configs import Config

from time import time

__all__ = ["get_confession"]


class GetConfession(ConfessionManager):

    def get(self):
        try:
            confession = self.db.docs.find(
                {
                    "post_time": {"$gte": int(time()) - Config.TIME_OUT_CONFESSION},
                    "status": "pending",
                    "send": False,
                },
                {"_id": 0, "confession": 1, "confession_id": 1},
            )
            list_confession = {}

            for docs in confession:

                confession_id = docs.get("confession_id", None)
                confession_text = docs.get("confession", None)

                if confession_id and confession_text:
                    list_confession[confession_id] = confession_text

            return list_confession
        except Exception as e:
            logger.error(e)


get_confession = GetConfession()
