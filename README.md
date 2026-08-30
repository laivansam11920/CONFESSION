# Hệ Thống Confession Ẩn Danh (Anonymous Confession Box)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-green.svg)](https://www.mongodb.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://aistudio.google.com/)

*(Bilingual README: Scroll down for English version | Kéo xuống để xem bản tiếng Anh)*

---

## 🇻🇳 TIẾNG VIỆT

### Giới thiệu
Dự án là một ứng dụng web cho phép mọi người gửi tâm sự (confession) hoàn toàn ẩn danh. Hệ thống được xây dựng trên môi trường local (máy cá nhân) sau đó có thể dễ dàng triển khai (deploy) lên [Render.com](https://render.com) hoặc các nền tảng đám mây tương tự. Điểm nhấn của dự án là khả năng tự động kiểm duyệt bằng AI (Google Gemini) và tự động đăng bài lên Facebook.

### Tính năng & Trạng thái cấu hình
Dưới đây là các tính năng chính và trạng thái bật/tắt mặc định (có thể tinh chỉnh lại trong file `configs.py` hoặc môi trường `.env`):

- **Kiểm duyệt bằng AI (AI Moderation):** Sử dụng mô hình `gemma-4-31b-it` để đánh giá an toàn, chấm điểm (0-100) dựa trên ngữ cảnh tinh vi.
  - *Trạng thái:* **Tùy chọn** (Mặc định: `TẮT` / `MODERATION_CONFESSION = False`).
- **Nhận diện chống Spam/Trùng lặp:** Phát hiện bài viết giống nhau (độ tương đồng > 64%) trong vòng 24 giờ.
  - *Trạng thái:* **Bật sẵn** (Mặc định: `BẬT` / `CHECK_SAME_DOCS = True`).
- **Gửi Confession Ẩn Danh & Lấy Email:** Cho phép nhận email phản hồi nếu người dùng muốn.
  - *Trạng thái:* **Tùy chọn** (Mặc định: `TẮT` / `GET_EMAIL = False`).
- **Theo dõi người dùng (Tracking):** Lưu IP và Browser Fingerprint (mã hóa an toàn) để chống lạm dụng.
  - *Trạng thái:* **Tùy chọn** (Mặc định: `TẮT` / `TRACKING_USER = False`).
- **Tự động đăng bài Facebook:** Tự động tổng hợp các confession đã duyệt và đăng qua Graph API. Tính năng này đi kèm cơ chế `self_ping` giúp web không bị ngủ đông trên các nền tảng cloud miễn phí.

### Cài đặt & Khởi chạy

Dự án tối ưu hóa cho môi trường phát triển trên Windows và sử dụng `gunicorn` *(hiểu đơn giản là một "người quản lý" xịn xò giúp trang web không bị sập khi có nhiều người truy cập cùng lúc)* để chạy thực tế.

**Cách 1: Cài đặt tự động (Đang phát triển)**
```bash
python install.py
```
*(Tính năng này sẽ tự động thiết lập môi trường ảo và cài thư viện. Hiện tại đang trong giai đoạn hoàn thiện).*

**Cách 2: Cài đặt thủ công (Khuyên dùng)**
1. **Clone dự án & Tạo môi trường ảo (Windows):**
   ```bash
   git clone <repository_url>
   cd <project_name>
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Cấu hình:** Cập nhật thông tin vào file `.env` (như `MONGO_URI`, `GOOGLE_AI_API_KEY`, `FACEBOOK_PAGE_ACCESS_TOKEN`, v.v.).
4. **Khởi chạy bằng Gunicorn (cho môi trường Render/Cloud):**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:2011 "app:app"
   ```
   *(Lệnh này gọi 4 "nhân viên" - worker - để cùng lúc xử lý yêu cầu, giúp web mượt hơn rất nhiều).*

---

## 🇬🇧 ENGLISH

### Introduction
This is an anonymous confession web application designed to be developed locally and deployed to cloud platforms like [Render.com](https://render.com). It features an automated AI-driven moderation system (Google Gemini) and Facebook Graph API integration for automatic publishing.

### Features & Default Configurations
- **AI Moderation:** Uses the `gemma-4-31b-it` model to deeply analyze intent and score content safety (0-100). 
  - *Status:* **Optional** (Default: `OFF` / `MODERATION_CONFESSION = False`).
- **Anti-Spam / Duplicate Detection:** Detects and merges similar posts (>64% similarity) within 24 hours.
  - *Status:* **Enabled** (Default: `ON` / `CHECK_SAME_DOCS = True`).
- **Email Collection:** Option for users to leave their email for notifications.
  - *Status:* **Optional** (Default: `OFF` / `GET_EMAIL = False`).
- **User Tracking (Security):** Encrypts and stores IP addresses and browser fingerprints to prevent abuse.
  - *Status:* **Optional** (Default: `OFF` / `TRACKING_USER = False`).
- **Facebook Auto-Posting:** Automatically posts approved confessions via Graph API. Includes a `self_ping` mechanism to keep free-tier cloud servers alive.

### Setup & Run

The project is actively developed in a Windows environment. It utilizes `gunicorn` for production deployment.

**Method 1: Auto-Installer (In Development)**
```bash
python install.py
```

**Method 2: Manual Setup (Recommended)**
1. **Clone & Virtual Environment (Windows):**
   ```bash
   git clone <repository_url>
   cd <project_name>
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Setup:** Provide `.env` variables (`MONGO_URI`, API keys, etc.).
4. **Run with Gunicorn (Production/Render):**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:2011 "app:app"
   ```
---
### Tác giả / Author
**Lại Văn Sâm**
&copy; 2026. Mọi bản quyền được bảo lưu.