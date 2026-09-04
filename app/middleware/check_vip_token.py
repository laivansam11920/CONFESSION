from app.database import db
from datetime import datetime, timezone
from pymongo import ReturnDocument


def is_vip_token(token) -> bool:
    data = (
        db.vip_key.find_one_and_update(
            {
                "key": token,
                "used": False,
                "expires_at": {
                    "$lte": datetime.now(timezone.utc),
                },
            },
            {
                "$set": {
                    "used": True,
                },
            },
            {"_id": 0, "used": 1},
            return_document=ReturnDocument.AFTER,
        )
        or {}
    )
    if data.get("used", False):
        return True
    return False
