from configs import Config
from app.database import db
from app.utils.logger import console
from app.base import PostFacebook

from requests import post

from flask_babel import gettext as _

__all__ = ["Facebook"]


class PostFacebookCommon(PostFacebook):

    url: str

    def __init__(self):
        super().__init__()
        self.long_line = "\n--------------------------------------\n"

    def post(self) -> bool:
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
                ).sort("cfs", -1)
                or {}
            )

            if not data:
                return False

            post_text: str = Config.TOPIC_SENTENCE
            _count_post: int = 0

            ignore_cfs_id = []

            for docs in data:

                cfs_count: str = docs.get("cfs") or "?"
                confession_text: str | None = docs.get("confession")
                admin_comment: str = docs.get("admin_comment", "")

                if not confession_text:
                    if confession_id := docs.get("confession_id", ""):
                        ignore_cfs_id.append(confession_id)
                    continue

                post_text += f"\n#cfs{cfs_count}\n"
                post_text += f"{confession_text}\n"
                post_text += f"-> {admin_comment}\n" if admin_comment else "\n"
                _count_post += 1

            if link_cfs_post := Config.RENDER_EXTERNAL_URL:
                post_text += self.long_line
                if g_name := Config.NAME_GROUP_USE_PROJECT:
                    post_text += _(f"Maintain: ") + f"{g_name}\n"
                post_text += _("link gửi confession: ") + f"{link_cfs_post}\n"

            payload = {"message": post_text, "access_token": self.page_access_token}

            if not _count_post:
                return False

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
