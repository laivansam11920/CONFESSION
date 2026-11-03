from .base import GetCfs
from app.core.db import get_database
from app.core.exceptions.confession import ConfessionNotFoundException
from app.models.confession import ConfessionDataSchema

from uuid import UUID


class GetNormalCfs(GetCfs):

    @staticmethod
    def get(cfs_id: UUID | None) -> ConfessionDataSchema:

        if cfs_id is None:
            raise ConfessionNotFoundException()

        db = get_database()

        _confession = (
            db.docs.find_one({"cfs_id": cfs_id}, {"_id": 0, "cfs_content": 1}) or {}
        )

        if not _confession or not _confession.get("cfs_content"):
            raise ConfessionNotFoundException(cfs_id=cfs_id)

        return ConfessionDataSchema(
            cfs_content=_confession.get("cfs_content", ""),
            cfs_id=cfs_id,
        )
