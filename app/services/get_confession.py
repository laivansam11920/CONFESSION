from app.schema.confession import ConfessionSchema
from app.database import db

__all__ = ["GetConfession"]


class GetConfession:

    @staticmethod
    def get(cfs_id: str | None) -> ConfessionSchema:

        confession = (
            db.docs.find_one(
                {"confession_id": cfs_id},
                {"_id": 0, "confession": 1, "confession_id": 1},
            )
            or {}
        )

        return ConfessionSchema(
            confession=str(confession.get("confession", "")),
            confession_id=str(confession.get("confession_id", "")),
            post_time=0,
            email="",
        )
