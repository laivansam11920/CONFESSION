"""
mô tả chức năng của post_facebook_vip:
- có khả năng đăng trực tiếp hoặc đăng vào 1 khoảng thời gian tự chọn
- có khả năng đính kèm ảnh vào bài viết
- không đính kèm #cfs-nums (hoặc có nếu muốn) (mặc định là không đính kèm #cfs-nums)
- giới hạn cao hơn cfs bình thường do admin tự tùy chỉnh
- được cấp 1 bài viết riêng trên facebook để thể hiện
"""

# TODO: sự dụng key đi kèm để xác thực xem có phải vip

from app.base import PostFacebook
from app.database import db
from app.schema.confession import ConfessionSchema
from app.utils.logger import console

from requests import post


class PostFacebookVip(PostFacebook):

    def __init__(self):
        super().__init__()

    @staticmethod
    def check(confession: ConfessionSchema | None = None) -> ConfessionSchema:

        if not confession:
            return ConfessionSchema(confession="", confession_id="", post_time=0)

        data = (
            db.docs.find_one(
                {
                    "confession_id": confession.confession_id,
                    "is_sponsor": True,
                    "safe_to_post": True,
                    "send": False,
                },
                {"_id": 0, "confession": 1, "sponsor_requirements": 1},
            )
            or {}
        )

        return ConfessionSchema(
            confession=data.get("confession", ""),
            sponsor_requirements=data.get("sponsor_requirements", {}),
            confession_id=confession.confession_id,
            post_time=0,
        )

    def post(self, confession: ConfessionSchema | None = None):

        data: ConfessionSchema = self.check(confession)

        if not data.confession:
            return False

        cfs = data.confession

        if data.sponsor_requirements.get("use_tag_cfs_reqs", False):
            cfs = ""

        payload = {"message": data.confession, "access_token": self.page_access_token}

        #TODO: xây dựng tính năng tự chọn thời gian post ở đây
        res = post(self.url, data=payload, timeout=5)
        fb_data = res.json()

        if res.status_code != 200:
            console.warning(
                f"Facebook post failed: {fb_data.get('error', {}).get('message')}"
            )
            return False

        db.docs.update_one(
            {"confession_id": data.confession_id},
            {"$set": {"send": True}},
        )

        return True
