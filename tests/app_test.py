from services.save_cfs.save_data import SaveData
from app.schema.confession import ConfessionSchema
from time import time
from uuid import uuid4

text = "Xin cha nha ban"

info = ConfessionSchema(
    confession=text,
    confession_id=str(uuid4()),
    post_time=int(time()),
)

SaveData().save_to_db(info)
