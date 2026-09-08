from app.base import MailService
from app.schema.confession import ConfessionSchema
from app.services.get_data.get_uncertain_cfs import GetData
from app.utils.logger import console
from app.database import db
from configs import Config

from requests import post
from secrets import token_urlsafe

from datetime import datetime, timezone, timedelta


class EmailJS(MailService):

    url: str
    service_id: str
    template_id: str
    public_key: str
    private_key: str

    def __init__(self):
        self.url = "https://api.emailjs.com/api/v1.0/email/send"
        self.service_id = Config.SERVICE_ID_EMAIL_JS
        self.template_id = Config.TEMPLATE_ID_EMAIL_JS
        self.public_key = Config.PUBLIC_KEY_EMAIL_JS
        self.private_key = Config.PRIVATE_KEY_EMAIL_JS

    def send_mail(self, email: str, confession_id: str) -> bool:
        try:
            if not Config.SEND_MAIL:
                return False

            if not email:
                return False

            confession: ConfessionSchema = GetData(confession_id)

            if not (
                confession.confession and confession.post_time and confession.ai_data
            ):
                return False

            token: str = token_urlsafe(32)

            data: dict = {
                "service_id": self.service_id,
                "template_id": self.template_id,
                "user_id": self.public_key,
                "accessToken": self.private_key,
                "template_params": {
                    "email": email,
                    "link": f"{Config.RENDER_EXTERNAL_URL}/moderation?token={token}",
                    "confession": confession.confession,
                    "post_time": confession.post_time,
                    "score": confession.ai_data.get("score", "?"),
                    "reason": confession.ai_data.get("reason", "?"),
                },
            }

            res = post(self.url, json=data, timeout=20)

            if res.status_code != 200:
                console.error(res.text)
                return False

            db.docs.update_one(
                {"confession_id": confession.confession_id},
                {
                    "$set": {
                        "token_moderation": {
                            "key_moderation": token,
                            "expire_time": datetime.now(timezone.utc)
                            + timedelta(minutes=15),
                        }
                    }
                },
            )

            return True
        except Exception as e:
            console.error(e)
            return False


Email = EmailJS()
