from app.base import ConfessionManager
from app.utils.logger import logger

class GetConfession(ConfessionManager):

    def get_confession(self):
        try:
            confession = self.db.docs.find(
                {"status": "pending", "send": False},
                {"_id": 0, "confession": 1, "confession_id": 1},
            )
            list_confession = {}

            for docs in confession:

                confession_id = docs.get("confession_id", None)
                confession = docs.get("confession", None)

                if confession_id and confession:
                    list_confession[confession_id] = confession

            return list_confession
        except Exception as e:
            logger.error(e)