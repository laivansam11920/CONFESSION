"""
mô tả chức năng của post_facebook_vip:
- có khả năng đăng trực tiếp hoặc đăng vào 1 khoảng thời gian tự chọn
- có khả năng đính kèm ảnh vào bài viết
- không đính kèm #cfs-nums (hoặc có nếu muốn) (mặc định là không đính kèm #cfs-nums)
- giới hạn cao hơn cfs bình thường do admin tự tùy chỉnh
- được cấp 1 bài viết riêng trên facebook để thể hiện
"""

from app.base import PostFacebook


class PostFacebookVip(PostFacebook):

    def __init__(self):
        super().__init__()

    def post(self): ...
