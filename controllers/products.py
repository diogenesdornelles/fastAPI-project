from typing import Dict, List
from services import ProductsService
from .interface import InterfaceEntitiesController


class ProductsController(InterfaceEntitiesController):
    def __init__(self):
        self.service: ProductsService = ProductsService()

    def get_all(self) -> List[Dict] | Dict:
        self.service.get_all()
        response: List[Dict] | Dict = self.service.all_products
        return response

    def get_one_by_id(self, _id: str) -> Dict:
        self.service.get_one_by_id(_id)
        response: Dict = self.service.product
        return response

    def create_one(self, product: Dict) -> Dict:
        self.service.create_one(product)
        response: Dict = self.service.create_result
        return response

    def update_one_by_id(self, updates: Dict) -> Dict:
        self.service.update_one_by_id(updates)
        response: Dict = self.service.update_result
        return response

    def delete_one_by_id(self, _id: str) -> Dict:
        self.service.delete_one_by_id(_id)
        response: Dict = self.service.delete_result
        return response
