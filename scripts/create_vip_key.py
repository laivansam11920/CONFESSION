from app.database import db

from secrets import token_urlsafe
from datetime import datetime, timedelta, timezone

def create_vip_key() -> str:
    """
    How to use(all allow command):

    - python -m scripts.create_vip_key
    - python create_vip_key.py
    - python scripts/create_vip_key.py

    """
    try:
        key = token_urlsafe(32)
        db.vip_key.insert_one({
            "key": key,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
            "used": False,
        })
        return f"key của bạn là: {key}"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print(create_vip_key())