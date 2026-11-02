# Confession Data Schema

| Key | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `confession_id` | `int` | Primary, Unique | ID định danh duy nhất của bài confession. |
| `confession_content` | `str` | Non-empty | Nội dung văn bản của confession do người dùng gửi. |