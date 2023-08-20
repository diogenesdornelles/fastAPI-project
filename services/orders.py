from typing import List, Dict, Any
from bson.objectid import ObjectId
from pymongo import errors
from pymongo.cursor import Cursor
from services import ClientsService, ProductsService
from database import DB
from .interface import IServices
from models import AddItem, RemoveItem, ProductUpdate, ChangeStatus, ClientId, OrderId, FullOrder


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
    def all(self) -> List[Dict]:
        return self.__all_orders

    @property
    def many(self) -> List[Dict]:
        return self.__orders

    @property
    def one(self) -> Dict:
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

    def get_one_by_id(self, _id: OrderId) -> None:
        try:
            response: Dict = self.database_orders.find_one({"_id": _id.to_objectid()})
            if response:
                self.__order: Dict = response
            else:
                self.__order: Dict = {'failed': 'order not founded',
                                      '_id': str(_id.order_id)}
        except errors.OperationFailure:
            self.__order: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__order: Dict = {'failed': 'an error has occurred'}

    def create_one(self, _id: ClientId) -> None | Dict:
        """
        Create a single order.
        :parameter: client_id: str = client ID.
        :return: Dict
        """
        self.client_service.get_one_by_id(_id, True)
        if 'failed' in self.client_service.one:
            return {'failed': 'client not founded',
                    '_id': _id.client_id}
        else:
            self.client_service.one['_id']: str = str(self.client_service.one['_id'])
        order: Dict = FullOrder(**{"client": self.client_service.one}).to_dict()
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

    def add_product(self, item: AddItem):
        order_id: str = item.order_id
        product_id: str = item.product_id
        self.get_one_by_id(item.get_orderid())
        if 'failed' in self.one:
            self.__update_result: Dict = {'failed': 'order_id not founded',
                                          '_id': order_id}
        else:
            self.product_service.get_one_by_id(product_id, True)
            if 'failed' in self.product_service.one:
                self.__update_result: Dict = {'failed': 'product not founded',
                                              '_id': item.product_id}
            else:
                if self.product_service.one['quantity'] >= item.quantity:
                    new_quantity: int = self.product_service.one['quantity'] - item.quantity
                    product_updates: ProductUpdate = ProductUpdate(product_id=item.product_id,
                                                                   quantity=new_quantity)
                    self.product_service.update_one_by_id(product_updates)
                    self.product_service.one['quantity'] = item.quantity
                    self.product_service.one['_id'] = str(self.product_service.one['_id'])
                    order_id: ObjectId = ObjectId(order_id)
                    query: Dict = {
                        "_id": order_id
                    }
                    update: Dict = {
                        "$push": {
                            "items": self.product_service.one,
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
                                                  'quantity_in_stock': self.product_service.one['quantity'],
                                                  'quantity_requested': item.quantity}

    def remove_product(self, item: RemoveItem):
        order_id: str = item.order_id
        product_id: str = item.product_id
        self.get_one_by_id(item.get_orderid())
        if 'failed' in self.one:
            self.__update_result: Dict = {'failed': 'order_id not founded',
                                          '_id': order_id}
        else:
            item_founded: Dict = [item for item in self.one['items'] if str(item['_id']) == product_id][0]
            if len(item_founded) < 1:
                self.__update_result: Dict = {'failed': 'product_id not founded',
                                              '_id': product_id}
            else:
                items_remaining: List[Dict] = [item for item in self.one['items'] if str(item['_id']) != product_id]
                update: Dict = {
                    "$set": {
                        "items": items_remaining,
                    }
                }
                try:
                    order_id: ObjectId = ObjectId(order_id)
                    response: int = self.database_orders.update_one({'_id': order_id}, update).modified_count
                    if response > 0:
                        self.product_service.get_one_by_id(product_id, True)
                        new_quantity: int = self.product_service.one['quantity'] + item_founded['quantity']
                        product_updates: ProductUpdate = ProductUpdate(product_id=product_id,
                                                                       quantity=new_quantity)
                        self.product_service.update_one_by_id(product_updates)
                        self.__update_result: Dict = {'success': 'item deleted', 'quantity': response}
                    else:
                        self.__update_result: Dict = {'failed': 'an error has occurred'}
                except errors.OperationFailure:
                    self.__update_result: Dict = {'failed': 'An error has occurred: database operation fails'}
                # generic error
                except Exception as error:
                    print(error)
                    self.__update_result: Dict = {'failed': 'an error has occurred'}

    def change_status(self, status: ChangeStatus):
        order_id: str = status.order_id
        status_str: str = status.status
        self.get_one_by_id(status.get_orderid())
        if 'failed' in self.one:
            self.__update_result: Dict = {'failed': 'order_id not founded',
                                          '_id': order_id}
        else:
            update: Dict = {
                "$set": {
                    "status": status_str,
                }
            }
            try:
                order_id: ObjectId = ObjectId(order_id)
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
                new_quantity: int = self.product_service.one['quantity'] + item['quantity']
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
