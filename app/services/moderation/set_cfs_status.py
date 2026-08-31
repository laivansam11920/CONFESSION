from app.database import db
from app.schema.ReturnSchema import ReturnSchema
from app.utils.get_cfs_count import cfs_nums
from configs import Config

import functools

__all__ = ["UpdateStatusModerationCfs"]


class UpdateStatusModerationCfs:

    @staticmethod
    def update_cfs_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            res: ReturnSchema = func(*args, **kwargs)

            if not res.success:
                return res

            data = (
                db.docs.find_one(
                    {
                        "confession_id": res.data.get("confession_id"),
                        "send": False,
                        "status": "approved",
                    },
                    {"_id": 0, "ai_data": 1},
                )
                or {}
            )

            ai_data = data.get("ai_data", {})
            score = ai_data.get("score")

            if ai_data["uncertain"]:
                ...
                return res

            if score and score > Config.MAX_MODERATION_SCORE:
                db.docs.update_one(
                    {"confession_id": res.data.get("confession_id")},
                    {"$set": {"safe_to_post": True, "cfs": cfs_nums()}},
                )

            return res

        return wrapper
