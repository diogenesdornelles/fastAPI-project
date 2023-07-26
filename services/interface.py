from abc import ABC, abstractmethod
from typing import List, Dict


class InterfaceEntitiesServices(ABC):
    @abstractmethod
    def get_all(self) -> None:
        pass

    @abstractmethod
    def get_one_by_id(self, _id: str) -> None:
        pass

    @abstractmethod
    def create_one(self, user: Dict) -> None:
        pass

    @abstractmethod
    def update_one_by_id(self, updates: Dict) -> None:
        pass

    @abstractmethod
    def delete_one_by_id(self, _id: str) -> None:
        pass
