from typing import Dict, List, Any
from bson.objectid import ObjectId
from pymongo import errors
from database import DB
from .interface import IServices, IPhoto
from models import Product, ProductUpdate, FullProduct, ProductQuery


class ProductsService(IServices, IPhoto):
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
    def all(self) -> List[Dict] | Dict:
        return self.__all_products

    @property
    def many(self) -> List[Dict]:
        return self.__products

    @property
    def one(self) -> Dict:
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

    def get_all(self) -> None:
        try:
            response: List[Dict] = self.database.find()
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_products: List[Dict] = response
            else:
                self.__all_products: List = []
        except errors.OperationFailure:
            self.__all_products: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__all_products: Dict = {'failed': 'An error has occurred'}

    def get_many(self, query: ProductQuery):
        params: Dict = query.params()
        try:
            response: List[Dict] = self.database.find(params)
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__products: List[Dict] = response
            else:
                self.__products: List = []
        except errors.OperationFailure:
            self.__products: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__products: Dict = {'failed': 'An error has occurred'}

    def get_one_by_id(self, _id: str, projection: bool = False) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            if projection:
                response: Dict = self.database.find_one({"_id": _id},
                                                        {'created_at': 0,
                                                         'photos': 0,
                                                         'last_modified': 0})
            else:
                response: Dict = DB.products.find_one({"_id": _id})
            if response:
                self.__product: Dict = response
            else:
                self.__product: Dict = {'failed': 'Product not founded',
                                        '_id': str(_id)}
        except errors.OperationFailure:
            self.__product: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__product: Dict = {'failed': 'An error has occurred'}

    def create_one(self, product: Product) -> None:
        product: FullProduct = FullProduct(**product.to_dict())
        product: Dict = product.to_dict()
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
        except errors.OperationFailure:
            self.__create_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__create_result: Dict = {'failed': 'An error has occurred'}

    def update_one_by_id(self, updates: ProductUpdate) -> None:
        updates: Dict = updates.params()
        all_updates: Dict = {
            "$set": updates
        }
        try:
            result: int = self.database.update_one({"_id": updates['_id']},
                                                   all_updates).modified_count
            self.__update_result: Dict = {'success': f'{result} product(s) updated'} if result > 0 \
                else {'failed': 'Product not updated',
                      '_id': str(updates['_id'])}
        except errors.DuplicateKeyError as error:
            self.__update_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__update_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except errors.OperationFailure:
            self.__update_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__update_result: Dict = {'failed': 'An error has occurred'}

    def delete_one_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            result: int = self.database.delete_one({"_id": _id}).deleted_count
            self.__delete_result: Dict = {'success': f'{result} product(s) deleted'} if result > 0 \
                else {'failed': 'Product not deleted',
                      '_id': str(_id)}
        except errors.OperationFailure:
            self.__delete_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__delete_result: Dict = {'failed': 'An error has occurred'}

    def insert_photo(self, photo_url: str) -> None:
        product_id: ObjectId = ObjectId(self.one['_id'])
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
        except errors.OperationFailure:
            self.__insert_new_photo_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__insert_new_photo_result: Dict = {'failed': 'An error has occurred'}

    def remove_photo(self, photo_url: str) -> None:
        product_id: ObjectId = ObjectId(self.one['_id'])
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
            self.__delete_photo_result: Dict = {'success': 'Photo removed',
                                                'quantity': result}
        except errors.OperationFailure:
            self.__delete_photo_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__delete_photo_result: Dict = {'failed': 'An error has occurred'}
