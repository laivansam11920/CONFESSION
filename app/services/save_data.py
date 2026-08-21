from app.database import Database as db
from app.schema.confession import ConfessionSchema

class SaveData:

    @staticmethod
    def save_to_db(confession_data: ConfessionSchema):

        _ = db.connet().confession_doc