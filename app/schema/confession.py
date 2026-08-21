from dataclasses import dataclass


@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    send: bool
    confession_id: str
    post_time: int
    same_post_count: int = 0
    status: str = "pending"


"""
confession: dùng để chứa confession text chính
send: thể hiện trạng thái đã gửi confession hay chưa, dạng bool 
status: khi ai quét (quét vi phạm cộng đồng, ...) sẽ trả về peding/approved, hệ thống sẽ dựa trên active để xem xét việc gửi confesion
confession_id: dùng để ngăn chặn các confession trùng lặp(cơ bản)
post_time: thời gian đăng lần cuối
same_post_count: gi lại những bài đăng có cùng nội dung(ký tự) với bài đăng hiện tại.
"""
