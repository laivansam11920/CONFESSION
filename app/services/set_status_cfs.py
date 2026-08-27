from app.database import db

import functools


class UpdateStatusModerationCfs:

    @staticmethod
    def update_cfs_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            data = db.docs.find(
                {"status": "approved", "send": False},
                {"_id": 0, "ai_data": 1},
            )

            for docs in data:
                ...

            return func(*args, **kwargs)

        return wrapper
