from configs import Config
from app.database import db
from app.utils.logger import console

from requests import post


class PostFacebook:

    page_id: str
    page_access_token: str
    url: str

    def __init__(self):
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.page_access_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN
        self.url = f"https://graph.facebook.com/v19.0/{self.page_id}/feed"

    def post(self):
        try:
            data = (
                db.docs.find(
                    {
                        "safe_to_post": True,
                        "send": False,
                    },
                    {"_id": 0, "confession": 1, "cfs": 1},
                )
                or {}
            )

            if not data:
                return False

            post_text: str = Config.TOPIC_SENTENCE

            for docs in data:

                cfs_count: str = docs.get("cfs") or "?"
                confession_text: str | None = docs.get("confession")

                if not confession_text:
                    continue

                post_text += f"#cfs{cfs_count} : {confession_text}\n"

            if g_name := Config.NAME_GROUP_USE_PROJECT:
                post_text += f"\nMaintain: {g_name}\n"

            payload = {"message": post_text, "access_token": self.page_access_token}

            res = post(self.url, data=payload, timeout=5)
            fb_data = res.json()

            if not res.status_code == 200:
                console.warning(
                    f"Facebook post failed: {fb_data.get('error', {}).get('message')}"
                )
                return False

            db.docs.update_many(
                {"safe_to_post": True, "status": "approved", "send": False},
                {"$set": {"send": True}},
            )

            return True

        except Exception as e:
            console.error(e)
            return False

Facebook = PostFacebook()