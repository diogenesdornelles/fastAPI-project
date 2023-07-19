from datetime import datetime
from typing import Dict, List, Any
from bson.objectid import ObjectId
from pymongo import errors
from database import DB


class ProductsService:
    def __init__(self):
        self.database = DB.products
        self.__all_products = []
        self.__products = []
        self.__product = {}
        self.__create_result = {}
        self.__update_result = {}
        self.__delete_result = {}
        self.__insert_new_photo_result = {}
        self.__delete_photo_result = {}

    @property
    def all_products(self) -> List[Dict] | Dict:
        return self.__all_products

    @property
    def products(self) -> List[Dict]:
        return self.__products

    @property
    def product(self) -> Dict:
        return self.__product

    @property
    def create_result(self) -> Dict:
        return self.__create_result

    @property
    def update_result(self) -> Dict:
        return self.__update_result

    @property
    def delete_result(self) -> Dict:
        return self.__delete_result

    @property
    def insert_new_photo_result(self) -> Dict:
        return self.__insert_new_photo_result

    @property
    def delete_photo_result(self) -> Dict:
        return self.__delete_photo_result

    def get_all_products(self) -> None:
        try:
            response: List[Dict] = self.database.find()
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_products: List[Dict] = response
            else:
                self.__all_products: List = []
        except Exception:
            self.__all_products: Dict = {'failed': 'An error has occurred'}

    def get_one_product_by_id(self, _id: str, projection: bool = False) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            if projection:
                response: Dict = self.database.find_one({"_id": _id},
                                                        {'created_at': 0,
                                                         'last_modified': 0})
            else:
                response: Dict = DB.products.find_one({"_id": _id})
            if response:
                self.__product: Dict = response
            else:
                self.__product: Dict = {'failed': 'Product not founded',
                                        '_id': str(_id)}
        except Exception:
            self.__product: Dict = {'failed': 'An error has occurred'}

    def create_one_product(self, product: Dict) -> None:
        product["created_at"]: datetime = datetime.now()
        product["last_modified"]: datetime = product["created_at"]
        try:
            response: Any = self.database.insert_one(product).inserted_id
            if response:
                self.__create_result: Dict = {'success': 'Created product',
                                              '_id': str(response)}
            else:
                self.__create_result: Dict = {'failed': 'Product not created'}
        except errors.DuplicateKeyError as error:
            self.__create_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__create_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except Exception:
            self.__create_result: Dict = {'failed': 'An error has occurred'}

    def update_one_product_by_id(self, updates: Dict) -> None:
        if 'product_id' in updates:
            _id: ObjectId = ObjectId(updates['product_id'])
            del updates['product_id']
        else:
            _id: ObjectId = ObjectId(updates["_id"])
            del updates["_id"]
        if 'photos' in updates:
            del updates['photos']
        updates["last_modified"]: datetime = datetime.now()
        all_updates: Dict = {
            "$set": updates
        }
        try:
            result: int = self.database.update_one({"_id": _id},
                                                   all_updates).modified_count
            self.__update_result: Dict = {'success': f'{result} product(s) updated'} if result > 0 \
                else {'failed': 'Product not updated',
                      '_id': str(_id)}
        except errors.DuplicateKeyError as error:
            self.__update_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__update_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except Exception:
            self.__update_result: Dict = {'failed': 'An error has occurred'}

    def delete_one_product_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            result: int = self.database.delete_one({"_id": _id}).deleted_count
            self.__delete_result: Dict = {'success': f'{result} product(s) deleted'} if result > 0 \
                else {'failed': 'Product not deleted',
                      '_id': str(_id)}
        except Exception:
            self.__delete_result: Dict = {'failed': 'An error has occurred'}

    def insert_new_photo_on_product(self, photo_url: str) -> None:
        product_id: ObjectId = ObjectId(self.product['_id'])
        query: Dict = {
            "_id": product_id
        }
        update: Dict = {
            "$push": {
                "photos": photo_url,
            }
        }
        try:
            result: int = self.database.update_one(query, update).modified_count
            self.__insert_new_photo_result: Dict = {'success': 'Photo inserted',
                                                    'quantity': result}
        except Exception:
            self.__insert_new_photo_result: Dict = {'failed': 'An error has occurred'}

    def remove_photo_from_product(self, photo_url: str) -> None:
        product_id: ObjectId = ObjectId(self.product['_id'])
        query: Dict = {
            "_id": product_id
        }
        pull: Dict = {
            "$pull": {
                "photos": photo_url
            }
        }
        try:
            result: int = self.database.update_one(query, pull).modified_count
            self.__insert_new_photo_result: Dict = {'success': 'Photo removed',
                                                    'quantity': result}
        except Exception:
            self.__delete_photo_result: Dict = {'failed': 'An error has occurred'}
