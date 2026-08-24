from app.services.moderation import moderation
from app.services.get_confession import get_confession
from dataclasses import asdict

tes_cfs = {"1": "tối học thêm về vào nhà nghỉ không? ngủ ở đó 1 hôm"}

res = moderation.check_confession(tes_cfs)
