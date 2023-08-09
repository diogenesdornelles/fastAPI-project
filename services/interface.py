from abc import ABC, abstractmethod
from typing import List, Dict


class IServices(ABC):

    @abstractmethod
    def all(self) -> List[Dict]:
        pass

    @abstractmethod
    def many(self) -> List[Dict]:
        pass

    @abstractmethod
    def one(self) -> Dict:
        pass

    @abstractmethod
    def create_result(self) -> Dict:
        pass

    @abstractmethod
    def update_result(self) -> Dict:
        pass

    @abstractmethod
    def delete_result(self) -> Dict:
        pass

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


class IPhoto(ABC):

    @abstractmethod
    def insert_new_photo_result(self) -> Dict:
        pass

    @abstractmethod
    def delete_photo_result(self) -> Dict:
        pass

    @abstractmethod
    def insert_photo(self, photo_url: str) -> None:
        pass

    @abstractmethod
    def remove_photo(self, photo_url: str) -> None:
        pass
