from app.database.Database import db
from app.schema.ReturnSchema import ReturnSchema
from app.utils.logger import console

from functools import wraps
from threading import Thread
from typing import Callable


class HumansModeration:

    @staticmethod
    def _update_confession(res: ReturnSchema) -> bool:
        try:
            db.docs.update_one(
                {
                    "confession_id": res.data.get("confession_id"),
                    "send": False,
                    "humans_check_safe": True,
                },
                {"$set": {"safe_to_post": True}},
            )
            return True
        except Exception as e:
            console.error(e)
            return False

    def check(self, func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):

            res: ReturnSchema = func(*args, **kwargs)
            Thread(target=lambda: self._update_confession(res), daemon=True).start()

            return res

        return wrapper
