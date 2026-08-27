from app.base import ConfessionManager

import functools


class UpdateStatusModerationCfs(ConfessionManager):

    def update_cfs_moderation(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            data = self.db.find(
                {"status": "approved", "send": False},
                {"_id": 0, "ai_data": 1},
            )

            for docs in data:
                ...

            return func(*args, **kwargs)

        return wrapper
