from app.database import Database as db
from app.schema.confession import ConfessionSchema
from app.utils.logger import logger
from app.utils.check_similar import is_similar
from configs import Config

from dataclasses import asdict
from time import time

class ConfessionManager:
    def __init__(self):
        self.db = db.connet()


class SaveData(ConfessionManager):

    def save_to_db(self, confession_data: ConfessionSchema) -> bool:
        try:
            confession_data_dict: dict = asdict(confession_data)

            if Config.CHECK_SAME_DOCS:

                old_docs = (
                    self.db.docs.find(
                        {"post_time": {"$gte": int(time()) - Config.TIME_OUT_CONFESSION}}
                    )
                    .sort("_id", -1)
                    .limit(100)
                )

                matched_id = None

                for doc in old_docs:
                    if is_similar(confession_data.confession, doc.get("confession", "")):
                        matched_id = doc["confession_id"]
                        break

                if matched_id:
                    self.db.docs.update_one(
                        {"confession_id": matched_id}, {"$inc": {"same_post_count": 1}}
                    )
                    return True

            self.db.docs.insert_one(confession_data_dict)
            return True

        except (Exception, KeyError) as e:
            logger.error(e)
            return False

# TODO: PHẢI LÀM SAO NẾU MỘT NGƯỜI SPAM NHIỀU CONFESSION NHƯNG KHÔNG THỂ XÁC NHẬN DANH TÍNH, CẦN SỰ DỤNG AI HOẶC CÁC CÔNG CỤ MẠNH, HOẶC NHỜ ĐẾN SỰ KIỂM DUYỆT CỦA CON NGƯỜI.
