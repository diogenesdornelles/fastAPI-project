from typing import List, Dict
from services import OrdersService
from .interface import IController
from models import AddItem, RemoveItem
from models import ChangeStatus


class OrdersController(IController):
    def __init__(self):
        self.service: OrdersService = OrdersService()

    def get_all(self) -> List[Dict]:
        self.service.get_all()
        response: List[Dict] = self.service.all
        return response

    def get_one_by_id(self, _id: str) -> Dict:
        self.service.get_one_by_id(_id)
        response: Dict = self.service.one
        return response

    def create_one(self, client_id: str) -> Dict:
        self.service.create_one(client_id)
        response: Dict = self.service.create_result
        return response

    def update_one_by_id(self, updates: Dict) -> Dict:
        pass

    def add_item(self, item: AddItem) -> Dict:
        self.service.add_product(item)
        response: Dict = self.service.update_result
        return response

    def remove_item(self, item: RemoveItem) -> Dict:
        self.service.remove_product(item)
        response: Dict = self.service.update_result
        return response

    def change_status(self, status: ChangeStatus) -> Dict:
        self.service.change_status(status)
        response: Dict = self.service.update_result
        return response

    def delete_one_by_id(self, _id: str) -> Dict:
        self.service.delete_one_by_id(_id)
        response: Dict = self.service.delete_result
        return response
