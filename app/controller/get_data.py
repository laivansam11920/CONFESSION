from abc import ABC, abstractmethod


class GetData(ABC):

    @abstractmethod
    def get_data(self):
        pass
