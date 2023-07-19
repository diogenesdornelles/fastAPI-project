from typing import Dict, List
from services import ProductsService


class ProductsController:
    def __init__(self):
        self.service: ProductsService = ProductsService()

    def get_all_products(self) -> List[Dict] | Dict:
        self.service.get_all_products()
        response: List[Dict] | Dict = self.service.all_products
        return response

    def get_one_product_by_id(self, _id: str) -> Dict:
        self.service.get_one_product_by_id(_id)
        response: Dict = self.service.product
        return response

    def create_one_product(self, product: Dict) -> Dict:
        self.service.create_one_product(product)
        response: Dict = self.service.create_result
        return response

    def update_one_product_by_id(self, updates: Dict):
        self.service.update_one_product_by_id(updates)
        response: Dict = self.service.update_result
        return response

    def delete_one_product_by_id(self, _id: str) -> Dict:
        self.service.delete_one_product_by_id(_id)
        response: Dict = self.service.delete_result
        return response
