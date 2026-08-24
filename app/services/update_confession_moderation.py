from .moderation import moderation
from .get_confession import get_confession
from app.extensions.threads import executor

import functools

__all__ = ["ConfessionModeration"]

class UpdateConfessionModeration:

    @staticmethod
    def check_confession_moderation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            if result.get("success", False):
                executor.submit(lambda: moderation.update_confession_moderation(get_confession.get()))

            return result
        return wrapper


ConfessionModeration = UpdateConfessionModeration()