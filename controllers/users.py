from typing import Dict, List
from services import UsersService


class UsersController:
    def __init__(self):
        self.service: UsersService = UsersService()

    def get_all_users(self) -> List[Dict]:
        self.service.get_all_users()
        response: List[Dict] = self.service.all_users
        return response

    def get_one_user_by_id(self, _id: str) -> Dict:
        self.service.get_one_user_by_id(_id)
        response: Dict = self.service.user
        return response

    def create_one_user(self, user: Dict):
        self.service.create_one_user(user)
        response: Dict = self.service.create_result
        return response

    def update_one_user_by_id(self, updated: Dict):
        self.service.update_one_user_by_id(updated)
        response: Dict = self.service.update_result
        return response

    def delete_one_user_by_id(self, _id: str) -> Dict:
        self.service.delete_one_user_by_id(_id)
        response: Dict = self.service.delete_result
        return response