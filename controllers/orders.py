from typing import List, Dict
from services import OrdersService
from .interface import InterfaceEntitiesController


class OrdersController(InterfaceEntitiesController):
    def __init__(self):
        self.service: OrdersService = OrdersService()

    def get_all(self) -> List[Dict]:
        self.service.get_all()
        response: List[Dict] = self.service.all_orders
        return response

    def get_one_by_id(self, _id: str):
        self.service.get_one_by_id(_id)
        response: Dict = self.service.order
        return response

    def create_one(self, order: Dict):
        self.service.create_one(order)
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
