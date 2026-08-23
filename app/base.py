from app.database import Database as db

from abc import ABC, abstractmethod
from typing import Any


class AiServices(ABC):
    def __init__(self, client: Any, model: str):
        self.client = client
        self.model = model

    @abstractmethod
    def check_confession(self, **list_confession):
        pass


class ConfessionManager:
    def __init__(self):
        self.db = db.connect()


class GetData(ABC):

    @abstractmethod
    def get_data(self):
        pass
