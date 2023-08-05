from datetime import datetime
from typing import List, Dict, Any
from bson.objectid import ObjectId
from pymongo import errors
from pymongo.cursor import Cursor
from services import ClientsService, ProductsService
from database import DB
from .interface import IServices
from models import Item, ProductUpdate, ChangeStatus


class OrdersService(IServices):
    def __init__(self):
        self.database_orders = DB.orders
        self.client_service: ClientsService = ClientsService()
        self.product_service: ProductsService = ProductsService()
        self.__all_orders = []
        self.__orders = []
        self.__order: Dict = {}
        self.__create_result = {}
        self.__update_result = {}
        self.__delete_result = {}

    @property
    def all_orders(self) -> List[Dict]:
        return self.__all_orders

    @property
    def orders(self) -> List[Dict]:
        return self.__orders

    @property
    def order(self) -> Dict:
        return self.__order

    @property
    def create_result(self) -> Dict:
        return self.__create_result

    @property
    def update_result(self) -> Dict:
        return self.__update_result

    @property
    def delete_result(self) -> Dict:
        return self.__delete_result

    def get_all(self) -> None:
        try:
            response: Cursor[Any] = self.database_orders.find()
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_orders: List[Dict] = response
            else:
                self.__all_orders: List = []
        except errors.OperationFailure:
            self.__all_orders: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__all_orders: Dict = {'failed': 'an error has occurred'}

    def get_one_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            response: Dict = self.database_orders.find_one({"_id": _id})
            if response:
                self.__order: Dict = response
            else:
                self.__order: Dict = {'failed': 'order not founded',
                                      '_id': str(_id)}
        except errors.OperationFailure:
            self.__order: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__order: Dict = {'failed': 'an error has occurred'}

    def create_one(self, order: Dict) -> None | Dict:
        """
        Create a single order.
        :param order: Dict = The order requested by client.
        :parameter: order.client_id: str = client ID.
        :return: Dict
        """
        self.client_service.get_one_by_id(order["client_id"], True)
        if 'failed' in self.client_service.client:
            return {'failed': 'client not founded',
                    '_id': order["client_id"]}
        else:
            self.client_service.client['_id']: str = str(self.client_service.client['_id'])
        order: Dict = {"items": [],
                       "client": self.client_service.client,
                       "status": 'in_cart',
                       "created_at": datetime.now(),
                       "last_modified": datetime.now(),
                       }
        try:
            response: Any = self.database_orders.insert_one(order).inserted_id
            if response:
                self.__create_result: Dict = {'success': 'order created',
                                              '_id': str(response)}
            else:
                self.__create_result: Dict = {'failed': 'an error has occurred'}
        except errors.OperationFailure:
            self.__create_result: Dict = {'failed': 'an error has occurred: database operation fails'}
            # generic error
        except Exception:
            self.__create_result: Dict = {'failed': 'an error has occurred'}

    def add_product(self, order_id: str, item: Item):
        self.get_one_by_id(order_id)
        if 'failed' in self.order:
            self.__update_result: Dict = {'failed': 'order_id not founded',
                                          '_id': order_id}
        else:
            self.product_service.get_one_by_id(item.product_id.to_str(), True)
            if 'failed' in self.product_service.product:
                self.__update_result: Dict = {'failed': 'product not founded',
                                              '_id': item.product_id}
            else:
                if self.product_service.product['quantity'] >= item.quantity:
                    new_quantity: int = self.product_service.product['quantity'] - item.quantity
                    product_updates: ProductUpdate = ProductUpdate(product_id=item.product_id,
                                                                   quantity=new_quantity)
                    self.product_service.update_one_by_id(product_updates)
                    self.product_service.product['quantity'] = item.quantity
                    self.product_service.product['_id'] = str(self.product_service.product['_id'])
                    order_id: ObjectId = ObjectId(order_id)
                    query: Dict = {
                        "_id": order_id
                    }
                    update: Dict = {
                        "$push": {
                            "items": self.product_service.product,
                        }
                    }
                    try:
                        response: int = self.database_orders.update_one(query, update).modified_count
                        self.__update_result: Dict = {'success': 'item inserted',
                                                      'quantity': response}
                    except errors.OperationFailure:
                        self.__update_result: Dict = {'failed': 'an error has occurred: database operation fails'}
                    # generic error
                    except Exception:
                        self.__update_result: Dict = {'failed': 'an error has occurred'}
                else:
                    self.__update_result: Dict = {'failed': 'product is not enough in stock',
                                                  '_id': item.product_id,
                                                  'quantity_in_stock': self.product_service.product['quantity'],
                                                  'quantity_requested': item.quantity}

    def remove_product(self, order_id: str, product_id: str):
        self.get_one_by_id(order_id)
        if 'failed' in self.order:
            self.__update_result: Dict = {'failed': 'order_id not founded',
                                          '_id': order_id}
        else:
            item_founded: Dict = [item for item in self.order['items'] if item['_id'] == product_id][0]
            if len(item_founded) < 1:
                self.__update_result: Dict = {'failed': 'product_id not founded',
                                              '_id': product_id}
            else:
                self.product_service.get_one_by_id(product_id, True)
                new_quantity: int = self.product_service.product['quantity'] + item_founded['quantity']
                product_updates: ProductUpdate = ProductUpdate(product_id=product_id,
                                                               quantity=new_quantity)
                self.product_service.update_one_by_id(product_updates)
                items: List[Dict] = [item for item in self.order['items'] if item['_id'] != product_id]
                update: Dict = {
                    "items": items,
                }
                try:
                    response: int = self.database_orders.update_one({'_id': order_id}, update).modified_count
                    self.__update_result: Dict = {'success': 'item deleted', 'quantity': response}
                except errors.OperationFailure:
                    self.__update_result: Dict = {'failed': 'An error has occurred: database operation fails'}
                # generic error
                except Exception:
                    self.__update_result: Dict = {'failed': 'an error has occurred'}

    def change_status(self, status: ChangeStatus):
        order_id: str = status.order_id.to_str()
        status: str = status.status.value()
        self.get_one_by_id(order_id)
        if 'failed' in self.order:
            self.__update_result: Dict = {'failed': 'order_id not founded',
                                          '_id': order_id}
        else:
            update: Dict = {
                "status": status,
            }
            try:
                response: int = self.database_orders.update_one({'_id': order_id}, update).modified_count
                self.__update_result: Dict = {'success': 'status modified', 'quantity': response}
            except errors.OperationFailure:
                self.__update_result: Dict = {'failed': 'An error has occurred: database operation fails'}
            # generic error
            except Exception:
                self.__update_result: Dict = {'failed': 'an error has occurred'}

    def update_one_by_id(self, updates: Dict) -> None:
        raise NotImplementedError('Method not implemented')

    def delete_one_by_id(self, order_id: str) -> None:
        try:
            # convert str to objectid
            order_id: ObjectId = ObjectId(order_id)
            # get order saved
            result: Dict = self.database_orders.find_one({"_id": order_id})
            # after exclude order, increase quantities in stock
            for item in result['items']:
                self.product_service.get_one_by_id(item['_id'], True)
                new_quantity: int = self.product_service.product['quantity'] + item['quantity']
                product_updates: ProductUpdate = ProductUpdate(product_id=item['product_id'],
                                                               quantity=new_quantity)
                self.product_service.update_one_by_id(product_updates)
            # exclude
            result: int = self.database_orders.delete_one({"_id": order_id}).deleted_count
            self.__delete_result: Dict = {'success': 'order deleted',
                                          'quantity': result} if \
                result > 0 else {'failed': 'order not deleted',
                                 '_id': str(order_id)}
        except errors.OperationFailure:
            self.__delete_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__delete_result: Dict = {'failed': 'An error has occurred'}
