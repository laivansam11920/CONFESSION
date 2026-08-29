from app.database import db
from pymongo import ReturnDocument


def cfs_nums() -> int:
    cfs_docs = db.cfs_count.find_one_and_update(
        {"id": "confession_id"},
        {"$inc": {"seq": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True,
    )
    return (cfs_docs or {}).get("seq", 1)
