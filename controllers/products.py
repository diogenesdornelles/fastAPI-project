from typing import Dict, List, Union
from services import ProductsService
from .interface import IController
from models import Product
from models import ProductUpdate, ProductQuery


class ProductsController(IController):
    def __init__(self):
        self.service: ProductsService = ProductsService()

    def get_all(self) -> List[Dict] | Dict:
        self.service.get_all()
        response: List[Dict] | Dict = self.service.all
        return response

    def get_one_by_id(self, _id: str) -> Dict:
        self.service.get_one_by_id(_id)
        response: Dict = self.service.one
        return response

    def get_many(self, query: ProductQuery) -> List[Dict] | Dict:
        self.service.get_many(query)
        response: List[Dict] = self.service.many
        return response

    def create_one(self, product: Product) -> Dict:
        self.service.create_one(product)
        response: Dict = self.service.create_result
        return response

    def update_one_by_id(self, updates: ProductUpdate) -> Dict:
        self.service.update_one_by_id(updates)
        response: Dict = self.service.update_result
        return response

    def delete_one_by_id(self, _id: str) -> Dict:
        self.service.delete_one_by_id(_id)
        response: Dict = self.service.delete_result
        return response
