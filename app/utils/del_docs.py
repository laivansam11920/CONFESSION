from app.database import db

import functools
import time


def del_docs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        one_week_ago = time.time() - (7 * 24 * 60 * 60)

        db.docs.delete_many(
            {
                "ai_data.uncertain": False,
                "post_time": {"$lt": one_week_ago},
                "$or": [{"send": True}, {"send": False, "safe_to_post": False}],
            }
        )

        return func(*args, **kwargs)

    return wrapper
