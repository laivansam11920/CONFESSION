from typing import Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.database import Database

from app.core.config import Config
from .base import DatabaseBase

__all__ = ["mongo_db", "get_database"]


class MongoDB(DatabaseBase):

    _client: MongoClient[Any] | None
    _db: Database[Any] | None

    def __init__(self) -> None:

        self._client = None
        self._db = None

    def connect(self) -> Database[Any]:

        if self._db is not None:
            return self._db

        try:

            client = MongoClient(
                Config.MONGO_URI,
                timeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                maxIdleTimeMS=45000,
                tz_aware=True,
            )

            client.admin.command("ping")
            db: Database[Any] = client[Config.NAME_DATABASE_MONGO]

            self._client = client
            self._db = db

            return self._db  # type: ignore

        except PyMongoError as e:
            self.disconnect()

            raise RuntimeError(f"Không thể kết nối đến Database: {e}") from e  # TODO

    def disconnect(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def get_db(self) -> Database[Any]:
        if self._db is None:
            return self.connect()
        return self._db

    def create_index(self):
        try:
            self._db.docs.create_index("cfs_id", unique=True, background=True)
        except PyMongoError:
            ...


mongo_db = MongoDB()


def get_database() -> Database[Any]:
    return mongo_db.get_db()
