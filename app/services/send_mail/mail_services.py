from app.base import MailService
from app.schema.confession import ConfessionSchema
from app.utils.logger import console
from configs import Config

from requests import post


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

    def send_mail(self, email: str, confession: ConfessionSchema) -> bool:
        try:
            if not Config.SEND_MAIL:
                return False

            if not email:
                return False

            data: dict = {
                "service_id": self.service_id,
                "template_id": self.template_id,
                "user_id": self.public_key,
                "accessToken": self.private_key,
                "template_params": {
                    "email": email,
                    "link": "xinchao.com",
                    "confession": confession.confession,
                    "post_time": confession.post_time,
                    "score": confession.ai_data.get("score", "?"),
                    "reason": confession.ai_data.get("reason", "?"),
                }
            }


            res = post(self.url, json=data, timeout=20)
            #TODO: làm 1 trang html lựa chọn có/không nhằm mục đích xác thực kèm link
            if res.status_code != 200:
                console.error(res.text)
                return False
            return True
        except Exception as e:
            console.error(e)
            return False