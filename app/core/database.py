from abc import ABC, abstractmethod
from typing import Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.database import Database

from app.core.config import Config


class DatabaseBase(ABC):

    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def get_db(self): ...


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

            self._client = MongoClient(
                Config.MONGO_URI,
                timeoutMS=5000,
                serverSelectionTimeoutMS=5000,
                maxIdleTimeMS=45000,
                tz_aware=True,
            )

            self._client.admin.command("ping")
            self._db = self._client[Config.NAME_DATABASE_MONGO]
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

mongo_db = MongoDB()

def get_database() -> Database[Any]:
    return mongo_db.get_db()