from app.utils.logger import console
from .moderation import moderation
from .get_confession import GetConfession as Confession
from app.extensions.threads import executor
from app.schema.ReturnSchema import ReturnSchema

import functools

__all__ = ["ConfessionModeration"]


class ConfessionModeration:

    @staticmethod
    def update_cfs_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:

                res: ReturnSchema = func(*args, **kwargs)

                if res.success:
                    executor.submit(
                        lambda: moderation.update_confession_moderation(
                            Confession.get(res.data.get("confession_id")),
                        )
                    )

                return res
            except Exception as e:
                console.error(e)

        return wrapper
