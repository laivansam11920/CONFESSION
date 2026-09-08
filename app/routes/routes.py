from flask import Blueprint, request

from app.extensions.limiter import limiter
from app.extensions.crfs import crfs
from configs import Config
from app.services.moderation.check_key import CheckKeyModerationService

__all__ = [
    "main_route",
    "get_data",
    "ping",
    "testing_route",
    "moderation",
]


main_route: Blueprint = Blueprint("main_route", __name__)
get_data: Blueprint = Blueprint("get_data", __name__)
ping: Blueprint = Blueprint("ping", __name__)
moderation: Blueprint = Blueprint("moderation", __name__)
testing_route: Blueprint = Blueprint("testing", __name__)

if Config.CHANGE_GET_DATA_BY_WEB:

    @main_route.route("/")
    @limiter.exempt
    def index():
        from flask import render_template

        return render_template("index.html")  # type: ignore

    @get_data.post("/submit-confession")
    def get_confession():
        from app.controller.get_data import get_data_web

        return get_data_web.get_data()


if Config.CHANGE_GET_DATA_BY_GOOGLE_FORM:

    @get_data.post("/submit-confession-form")
    @crfs.exempt
    @limiter.limit(
        Config.DEFAULT_RATE_LIMIT,
        exempt_when=lambda: request.headers.get("X-App-Secret") == Config.SECRET_KEY,
    )
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


@moderation.route("/moderation", methods=["POST", "GET", "DELETE"])
@CheckKeyModerationService.check
def moderation_route(key_success: bool, cfs_id: str):
    from flask import render_template

    from app.services.get_data.get_uncertain_cfs import GetData

    if request.method == "GET":
        if not key_success:
            return render_template("moderation/action.html",
                               confession=None,
                               post_time=00.00,
                               score=0,
                               reason=None,
                               )

        data = GetData.get(cfs_id=cfs_id)

        return render_template("moderation/action.html",
                               confession=data.confession,
                               post_time=data.post_time,
                               score=data.ai_data.get("score", "?"),
                               reason=data.ai_data.get("reason", "?"),
                               )
    from app.services.update_cfs.update_uncertain import UpdateUncertain
    from flask import flash, redirect, url_for
    if request.method == "POST":


        UpdateUncertain.update_uncertain(cfs_id=cfs_id, safe_to_post=True)
        flash("thành công chấp thuận confession")
        return redirect(url_for("moderation.moderation_route"))

    UpdateUncertain.update_uncertain(cfs_id=cfs_id, safe_to_post=False)
    flash("Đã xóa thành công confession")
    return redirect(url_for("moderation.moderation_route"))
