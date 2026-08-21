from app.database import Database as db
from app.schema.confession import ConfessionSchema
from app.utils.logger import logger
from configs import Config


from dataclasses import asdict

from pymongo import ReturnDocument

class ConfessionManager:
    def __init__(self):
        self.db = db.connet()


class SaveData(ConfessionManager):

    def save_to_db(self, confession_data: ConfessionSchema) -> bool:
        try:
            confession_data_dict: dict = asdict(confession_data)

            if Config.CHECK_SAME_DOCS:

                self.db.docs.find_one_and_update(
                    {"confession_id": confession_data.confession_id},
                    {
                        "$inc": {"same_post_count": 1},
                        "$setOnInsert": confession_data_dict
                    },
                    upsert=True,
                    return_document=ReturnDocument.AFTER
                )
                return True

            self.db.docs.insert_one(confession_data_dict)
            return True

        except Exception as e:
            logger.error(e)
            return False
