"""
mô tả tính năng: xóa bài fb khi admin nhập key vào comment fb
khi admin nhập key thì key đó sẽ hủy ngay lập tức
khi truy vấn db bắt buộc phải dùng findOneAndUpdate
"""

from .create_key_del import CreateKeyDelPost as KeyDelete
from app.database import db
from app.utils.check_similar import is_similar


class DelPostFacebook:

    def del_post_facebook(self): ...
