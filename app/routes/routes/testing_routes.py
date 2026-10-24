from flask import Blueprint

__all__ = ["testing_route"]

testing_route: Blueprint = Blueprint("testing", __name__)


# @testing_route.route("/get_comment_post")
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
