from app.base import GetCfs
from app.database import db
from app.utils.logger import console
from app.schema.confession import ConfessionSchema


class GetUncertainCFS(GetCfs):

    @staticmethod
    def get(cfs_id: str | None) -> ConfessionSchema:
        try:

            if not cfs_id:
                return ConfessionSchema(confession="", confession_id="", post_time=0)

            res = (
                db.docs.find_one(
                    {"confession_id": cfs_id},
                    {"_id": 0, "confession": 1, "post_time": 1, "ai_data": 1},
                )
                or {}
            )

            return ConfessionSchema(
                confession=res.get("confession", ""),
                confession_id=cfs_id,
                post_time=res.get("post_time", 0),
                ai_data=res.get("ai_data", {}),
            )

        except Exception as e:
            console.error(e)
            return ConfessionSchema(confession="", confession_id="", post_time=0)


GetData = GetUncertainCFS()
