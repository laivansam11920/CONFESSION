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


class PostFacebookVip(PostFacebook):

    def __init__(self):
        super().__init__()

    @staticmethod
    def check(confession: ConfessionSchema):

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

        return data.get("confession"), data.get("sponsor_requirements", {})

    def post(self): ...
