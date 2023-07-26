from typing import Dict, List
from services import UsersService
from .interface import InterfaceEntitiesController


class UsersController(InterfaceEntitiesController):
    def __init__(self):
        self.service: UsersService = UsersService()

    def get_all(self) -> List[Dict]:
        self.service.get_all()
        response: List[Dict] = self.service.all_users
        return response

    def get_one_by_id(self, _id: str) -> Dict:
        self.service.get_one_by_id(_id)
        response: Dict = self.service.user
        return response

    def create_one(self, user: Dict):
        self.service.create_one(user)
        response: Dict = self.service.create_result
        return response

    def update_one_by_id(self, updates: Dict):
        self.service.update_one_by_id(updates)
        response: Dict = self.service.update_result
        return response

    def delete_one_by_id(self, _id: str) -> Dict:
        self.service.delete_one_by_id(_id)
        response: Dict = self.service.delete_result
        return response
