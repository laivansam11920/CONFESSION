from app.database import db
from app.utils.logger import console


class UpdateUncertain:

    @staticmethod
    def update_uncertain(cfs_id: str | None, safe_to_post: bool) -> bool:
        try:

            if not cfs_id:
                return False

            db.docs.update_one(
                {"confession_id": cfs_id},
                {"$set": {"safe_to_post": safe_to_post}},
            )

            return True

        except Exception as e:
            console.error(e)
            return False
