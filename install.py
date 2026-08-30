import questionary
import os
import secrets


def main():
    print("Confession setup tool", flush=True)

    env_data = {}

    env_data["MONGO_URI"] = questionary.text("Hãy nhập MONGO URI của bạn(Bắt buộc): ").ask()
    env_data["SECRET_KEY"] = secrets.token_hex(32)

    print("\n")

    use_ai = questionary.confirm(
        "Bạn có muốn bật tính năng kiểm duyệt bằng AI?\n"
        "(Lợi ích): Chúng tôi cung cấp hệ thống prompt để xử lý những câu nói vi phạm, mỉa mai ẩn dụ."
    ).ask()

    print("\n")

    if use_ai:
        env_data["GOOGLE_AI_API_KEY"] = questionary.text("Hãy nhập AI API KEY của bạn(Bắt buộc): ").ask()
        print("\n")
        env_data["MAX_MODERATION_SCORE"] = questionary.text(
            "Điểm tối đa của 1 confession (Nếu điểm AI chấm thấp hơn mức này thì confession đó sẽ bị chặn)\n"
            "Tìm hiểu thêm trong docs/moderation_by_ai.md hoặc app/prompts/moderation.py để biết thêm về cách tính điểm:",
            default="55.0"
        ).ask()




if __name__ == "__main__":
    main()