from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.synchronous.database import Database

from configs import Config
from app.utils.logger import console

__all__ = ["db"]


try:
    client: MongoClient[Any] = MongoClient(
        Config.MONGO_URI,
        timeoutMS=5000,
        serverSelectionTimeoutMS=5000,
        maxIdleTimeMS=45000,
    )
    client.admin.command("ping")
    db: Database[Any] = client[Config.MONGO_MAIN_DB]
except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
    console.error(e)
