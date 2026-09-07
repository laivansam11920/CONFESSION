from app.services.send_mail.mail_services import EmailJS
from app.schema.confession import ConfessionSchema

send_mail = EmailJS()

print(send_mail.send_mail("laivansam11920@gmail.com", ConfessionSchema(confession="afsaaf", confession_id="afsfasdf", post_time=111)))
