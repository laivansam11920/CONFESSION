from app.database import db

import functools

def del_docs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        db.docs.delete_many({
            "send": True,
            "ai_data.uncertain": False,
        })

        return func(*args, **kwargs)
    return wrapper
