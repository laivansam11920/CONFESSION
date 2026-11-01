from abc import ABC, abstractmethod


class DatabaseBase(ABC):

    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def get_db(self): ...
