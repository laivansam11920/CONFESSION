from .Database import db

db.docs.create_index([("send", 1), ("_id", -1), ("post_time", -1)])
