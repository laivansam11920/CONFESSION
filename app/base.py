from app.database import Database as db
from abc import ABC, abstractmethod


class AiServices(ABC):

    @abstractmethod
    def check_confession(self, list_confession: list):
        pass


class ConfessionManager:
    def __init__(self):
        self.db = db.connect()


class GetData(ABC):

    @abstractmethod
    def get_data(self):
        pass
