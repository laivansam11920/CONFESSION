from app.services.moderation import moderation
from app.services.get_confession import get_confession


print(moderation.check_confession(get_confession.get()))