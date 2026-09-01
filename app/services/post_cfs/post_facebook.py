from configs import Config
from app.database import db
from app.utils.logger import console
from app.base import PostFacebook

from requests import post

__all__ = ["Facebook"]


class PostFacebookCommon(PostFacebook):

    page_id: str
    page_access_token: str
    url: str

    def __init__(self):
        super().__init__()
        self.url = f"https://graph.facebook.com/v19.0/{self.page_id}/feed"

    def post(self):
        try:
            data = (
                db.docs.find(
                    {
                        "safe_to_post": True,
                        "send": False,
                    },
                    {
                        "_id": 0,
                        "confession": 1,
                        "cfs": 1,
                        "admin_comment": 1,
                        "confession_id": 1,
                    },
                )
                or {}
            )

            if not data:
                return False

            post_text: str = Config.TOPIC_SENTENCE

            ignore_cfs_id = []

            for docs in data:

                cfs_count: str = docs.get("cfs") or "?"
                confession_text: str | None = docs.get("confession")
                admin_comment: str = docs.get("admin_comment", "")

                if not confession_text:
                    if confession_id := docs.get("confession_id", ""):
                        ignore_cfs_id.append(confession_id)
                    continue

                post_text += f"\n#cfs{cfs_count} : {confession_text}{f"\n-> {admin_comment}" if admin_comment else ""}"

            if g_name := Config.NAME_GROUP_USE_PROJECT:
                post_text += f"\nMaintain: {g_name}\n"

            if link_cfs_post := Config.RENDER_EXTERNAL_URL:
                post_text += f"link gửi confession: {link_cfs_post}\n"

            payload = {"message": post_text, "access_token": self.page_access_token}

            res = post(self.url, data=payload, timeout=5)
            fb_data = res.json()

            if res.status_code != 200:
                console.warning(
                    f"Facebook post failed: {fb_data.get('error', {}).get('message')}"
                )
                return False

            db.docs.update_many(
                {
                    "safe_to_post": True,
                    "send": False,
                    "confession_id": {"$nin": ignore_cfs_id},
                },
                {"$set": {"send": True}},
            )

            return True

        except Exception as e:
            console.error(e)
            return False


Facebook = PostFacebookCommon()
