from flask import Blueprint

from app.extensions.limiter import limiter
from app.extensions.crfs import crfs
from configs import Config

__all__ = [
    "main_route",
    "get_data",
    "ping",
    "testing_route",
]


main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)
ping: Blueprint = Blueprint("ping", __name__)
testing_route: Blueprint = Blueprint("testing", __name__)

if Config.CHANGE_GET_DATA_BY_WEB:
    @main_route.route("/")
    @limiter.exempt
    def index():
        from flask import render_template

        return render_template("index.html")  # type: ignore


    @get_data.post("/submit-confession")
    def get_confession():
        """TODO:
        sự dụng redis để tạo 1 token có thời hạn trong vài phút, sau đó sẽ tính res/token để rate limit.
        ví dụ: 1 token chỉ được chứa duy nhất 1 cfs được gửi đi trong giờ, trong ngày, trong tháng, ... có custom.
        """
        from app.controller.get_data import get_data_web

        return get_data_web.get_data()

if Config.CHANGE_GET_DATA_BY_GOOGLE_FORM:
    @get_data.post("/submit-confession-form")
    @crfs.exempt
    def get_confession_form():
        from app.controller.get_data import get_data_google

        return get_data_google.get_data()


@testing_route.route("/get_comment_post")
def get_comment_post():
    """from flask import request, jsonify
    from configs import Config

    VERIFY_TOKEN = Config.SECRET_KEY

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Verification token mismatch", 403
        return "Invalid verification request", 400

    elif request.method == "POST":
        data = request.json()

        print(data, flush=True)

        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "feed":
                        value = change.get("value", {})

                        if value.get("item") == "comment" and value.get("verb") == "add":
                            comment_id = value.get("comment_id")
                            post_id = value.get("post_id")
                            message = value.get("message")
                            sender_name = value.get("from", {}).get("name")

                            print(f"Comment mới từ {sender_name} trên bài {post_id}: {message} (ID: {comment_id})", flush=True)

            return jsonify({"status": "EVENT_RECEIVED"}), 200
        return jsonify({"status": "ignored"}), 404"""
    # TODO: add 1 nick nào đó làm tester
    return {"success": True}


@ping.route("/ping")
@limiter.exempt
def ping_route():
    return {"success": True}
