import requests
from configs.configs import Config

# 1. Điền thông tin cấu hình của og vào đây
PAGE_ID = Config.FACEBOOK_PAGE_ID  # Thay bằng ID Fanpage vừa lấy
PAGE_ACCESS_TOKEN = (
    Config.FACEBOOK_PAGE_ACCESS_TOKEN
)  # Thay bằng Page Access Token vừa lấy


def post_confession_to_facebook(content: str, is_pending: bool = False) -> None:
    """
    Hàm gửi bài viết lên Facebook Fanpage qua Graph API.
    - is_pending = False: Đăng công khai luôn (Bài điểm cao)
    - is_pending = True: Lưu vào hàng chờ duyệt (Bài điểm lấp lửng)
    """
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"

    payload = {"message": content, "access_token": PAGE_ACCESS_TOKEN}

    try:
        response = requests.post(url, data=payload)
        data = response.json()

        if response.status_code == 200:
            post_id = data.get("id")
            if is_pending:
                print(f"✅ Đã gửi bài vào hàng chờ duyệt! ID: {post_id}")
            else:
                print(f"🚀 Đăng bài thành công lên Fanpage! Post ID: {post_id}")
        else:
            print(f"❌ Lỗi từ Facebook API: {data.get('error', {}).get('message')}")

    except Exception as e:
        print(f"❌ Lỗi kết nối Server: {e}")


# ==================== DEMO CHẠY THỬ ====================
if __name__ == "__main__":
    # Test 1: Đăng trực tiếp cfs sạch
    cfs_text_clean = "[#CFS101] Tối nay 9h hẹn crush ở Góc Cây Bàng..."
    post_confession_to_facebook(content=cfs_text_clean, is_pending=False)

    # Test 2: Đẩy bài nghi vấn vào hàng chờ Pending
    cfs_text_suspect = "[#CFS102] Bài này điểm AI thấp, cần Admin ngó qua..."
    post_confession_to_facebook(content=cfs_text_suspect, is_pending=True)
