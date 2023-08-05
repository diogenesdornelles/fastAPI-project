from abc import ABC, abstractmethod
from typing import List, Dict


class IController(ABC):
    @abstractmethod
    def get_all(self) -> List[Dict]:
        pass

    @abstractmethod
    def get_one_by_id(self, _id: str) -> Dict:
        pass

    @abstractmethod
    def create_one(self, user: Dict) -> Dict:
        pass

    @abstractmethod
    def update_one_by_id(self, updates: Dict) -> Dict:
        pass

    @abstractmethod
    def delete_one_by_id(self, _id: str) -> Dict:
        pass
