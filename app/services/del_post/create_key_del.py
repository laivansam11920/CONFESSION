from app.database import db
from app.utils.logger import console

from secrets import token_urlsafe


class CreateKeyDelPost:

    @staticmethod
    def create() -> dict:
        try:
            data = db.del_key.find_one_and_update(
                {"id": "del_key"},
                {
                    "$set": {
                        "key": str(token_urlsafe(32)),
                        "is_used": False,
                    }
                },
                {"_id": 0,"id": 0, "key": 1, "is_used": 1},
                upsert=True,
            ) or {}
            return data
        except Exception as e:
            console.error(e)
            return {}