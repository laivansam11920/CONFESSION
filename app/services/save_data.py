from app.database import Database as db
from app.schema.confession import ConfessionSchema

class SaveData:

    def __init__(self):
        self.db = db.connet()

    def save_to_db(self, confession_data: ConfessionSchema):

        _if_exits = self.db.docs.find_one_and_update(
            {"confession_id": confession_data.confession_id},
            {"$inc": {"same_post_count": 1}},
        )

