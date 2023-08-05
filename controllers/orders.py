from typing import List, Dict
from services import OrdersService
from .interface import IController
from models import Item
from models import ChangeStatus


class OrdersController(IController):
    def __init__(self):
        self.service: OrdersService = OrdersService()

    def get_all(self) -> List[Dict]:
        self.service.get_all()
        response: List[Dict] = self.service.all_orders
        return response

    def get_one_by_id(self, _id: str) -> Dict:
        self.service.get_one_by_id(_id)
        response: Dict = self.service.order
        return response

    def create_one(self, order: Dict) -> Dict:
        self.service.create_one(order)
        response: Dict = self.service.create_result
        return response

    def update_one_by_id(self, updates: Dict) -> Dict:
        pass

    def add_item(self, order_id: str, item: Item) -> Dict:
        self.service.add_product(order_id, item)
        response: Dict = self.service.update_result
        return response

    def remove_item(self, order_id: str, product_id: str) -> Dict:
        self.service.remove_product(order_id, product_id)
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
