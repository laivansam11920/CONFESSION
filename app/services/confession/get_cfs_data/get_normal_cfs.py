from .base import GetCfs
from app.core.db import get_database

from uuid import UUID


class GetNormalCfs(GetCfs):

    @staticmethod
    def get(cfs_id: UUID | None):

        if cfs_id is None:
            ...

        db = get_database()
