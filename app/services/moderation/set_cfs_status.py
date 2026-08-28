from app.database import db
from configs import Config

import functools


class UpdateStatusModerationCfs:

    @staticmethod
    def update_cfs_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            res = func(*args, **kwargs)

            if not Config.MODERATION_CONFESSION:
                return res

            data = db.docs.find(
                {"status": "approved", "send": False},
                {"_id": 0, "ai_data": 1, "confession_id": 1},
            )

            for docs in data:

                flag = False

                ai_data = docs["ai_data"]


                if ai_data["uncertain"]:
                    ...

                if ai_data["score"] <= Config.MAX_MODERATION_SCORE:
                    flag = True

                db.docs.update_one(
                    {"confession_id": docs["confession_id"]},
                    {
                        "$set": {
                            "safe_to_post": flag,
                        }
                    },
                )

            return res

        return wrapper
