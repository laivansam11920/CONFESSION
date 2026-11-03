from abc import ABC, abstractmethod

from uuid import UUID


class GetCfs(ABC):

    @staticmethod
    @abstractmethod
    def get(cfs_id: UUID | None): ...
