from app.utils.logger import console
from configs import Config
from app.database import db

from time import time

__all__ = ["GetConfession"]


class GetConfession:

    @staticmethod
    def get() -> dict:
        try:
            confession = db.docs.find(
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
            console.error(e)
            return {}
