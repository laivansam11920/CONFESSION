
```python
#app/schema/confession.py
from dataclasses import dataclass

@dataclass(frozen=True)
class ConfessionSchema:
    confession: str
    confession_id: str
    post_time: int
    email: str
    same_post_count: int = 0
    status: str = "pending"
    send: bool = False
```
###

```python
confession: str
``` 
**confession**: dùng để chứa confession text chính

---
```python
confession_id: str
```
**confession_id**: dùng để ngăn chặn các confession trùng lặp(cơ bản)

---
```python
post_time: int
```
**post_time**: thời gian đăng lần cuối

---
```python
email: str
```
**email**: dùng để lưu email của người dùng. Mặc định là **anonymous** 

---
```python
same_post_count: int = 0
```
**same_post_count**: gi lại những bài đăng có cùng nội dung(ký tự) với bài đăng hiện tại.

---
```python
status: str = "pending"
```
**status**: khi ai quét (quét vi phạm cộng đồng, ...) sẽ trả về peding/approved, hệ thống sẽ dựa trên active để xem xét việc gửi confesion

---
```python
send: bool = False
```
**send**: thể hiện trạng thái đã gửi confession hay chưa, dạng bool

###