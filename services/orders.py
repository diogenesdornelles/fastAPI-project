from datetime import datetime
from typing import List, Dict, Any, Optional
from bson.objectid import ObjectId
from pymongo import errors
from pymongo.cursor import Cursor
from services import ClientsService, ProductsService
from database import DB
from .interface import InterfaceEntitiesServices


class MakeOrder:
    def __init__(self,
                 client_id: str = None,
                 items: list = None,
                 status: str = 'in_cart'):
        self.client_id: str = client_id
        self.items_ordered: List[Dict] = items
        self.status: str = status
        self.client: Dict = {}
        self.all_create: Dict = {}
        self.client_service: ClientsService = ClientsService()
        self.product_service: ProductsService = ProductsService()
        self.items_saved: List = []
        self.ables_to_save: List = []
        self.not_ables_to_save: List = []
        self.quantities_of_ables_to_save: List = []
        self.decrease_quantity_result: Dict = {}
        self.set_client()
        self.set_items()

    @property
    def get(self) -> Dict:
        # fill keys
        self.all_create['client']: Dict = self.client
        self.all_create['items']: List = []
        for item in self.ables_to_save:
            self.all_create['items'].append(item)
        self.all_create['status']: str = self.status
        self.all_create['created_at']: datetime = datetime.now()
        self.all_create['last_modified']: datetime = datetime.now()
        return self.all_create

    def set_client(self) -> None:
        # get client info
        self.client_service.get_one_client_by_id(self.client_id, True)
        if 'failed' in self.client_service.client:
            self.client: Dict = {'failed': 'Client not founded'}
        else:
            self.client_service.client['_id']: str = str(self.client_service.client['_id'])
            self.client: Dict = self.client_service.client

    def set_items(self):
        for item in self.items_ordered:
            # get product saved on db
            self.product_service.get_one_product_by_id(item['product_id'], True)
            # if not failed
            if 'failed' not in self.product_service.product:
                # verify if quantity on db is enough
                if self.product_service.product['quantity'] >= item['quantity']:
                    # insert quantities on db to decrease after
                    self.quantities_of_ables_to_save.append(self.product_service.product['quantity'])
                    # replace quantity on db by quantity ordered
                    self.product_service.product['quantity']: int = item['quantity']
                    # convert _id to str
                    self.product_service.product['_id']: str = str(self.product_service.product['_id'])
                    # products ables to save
                    self.ables_to_save.append(self.product_service.product)
                else:
                    self.not_ables_to_save.append({'failed': 'item is not enough',
                                                   'item': item['product_id']})
            else:
                self.not_ables_to_save.append({'failed': 'item not founded',
                                               'item_id': item['product_id']})

    def decrease_quantity_product(self) -> None:
        try:
            for index, item in enumerate(self.ables_to_save):
                new_quantity: int = self.quantities_of_ables_to_save[index] - item['quantity']
                self.product_service.update_one_product_by_id({"_id": item['_id'],
                                                               "quantity": new_quantity})
        except Exception:
            self.decrease_quantity_result: Dict = {'failed': 'An error has occurred'}


class UpdateOrder:
    def __init__(self,
                 order: Dict,
                 client_id: str = None,
                 items: list = None,
                 status: str = None):
        self.order_saved: Dict = order
        self.client_id: str = client_id
        self.items_ordered: List[Dict] = items
        self.status: str = status
        self.client: Dict = {}
        self.all_updates: Dict = {}
        self.client_service: ClientsService = ClientsService()
        self.product_service: ProductsService = ProductsService()
        self.items_saved: List = []
        self.ables_to_save: List = []
        self.not_ables_to_save: List = []
        self.quantities_of_ables_to_save: List = []
        self.decrease_quantity_result: Dict = {}
        self.set_client()
        self.set_status()
        self.restore_quantities()
        self.set_items()

    @property
    def get(self) -> Dict:
        self.all_updates['last_modified']: datetime = datetime.now()
        return self.all_updates

    def set_client(self) -> None:
        if isinstance(self.client_id, str):
            self.client_service.get_one_client_by_id(self.client_id, True)
            if 'failed' not in self.client_service.client:
                self.client: Dict = self.client_service.client
                self.all_updates['client']: Dict = self.client
            else:
                self.client = {'failed': 'Client not founded'}

    def set_status(self) -> None:
        if isinstance(self.status, str):
            self.all_updates['status']: str = self.status

    def restore_quantities(self) -> None:
        if len(self.items_ordered) > 0:
            for item in self.order_saved['items']:
                self.product_service.get_one_product_by_id(item['_id'], True)
                new_quantity: int = self.product_service.product['quantity'] + item['quantity']
                self.product_service.update_one_product_by_id({"_id": item['_id'],
                                                               "quantity": new_quantity})

    def set_items(self):
        if len(self.items_ordered) > 0:
            for item in self.items_ordered:
                self.product_service.get_one_product_by_id(item['product_id'], True)
                if 'failed' not in self.product_service.product:
                    if self.product_service.product['quantity'] >= item['quantity']:
                        self.quantities_of_ables_to_save.append(self.product_service.product['quantity'])
                        self.product_service.product['quantity']: int = item['quantity']
                        self.ables_to_save.append(self.product_service.product)
                    else:
                        self.not_ables_to_save.append({'failed': 'item is not enough',
                                                       'item': item['product_id']})
                else:
                    self.not_ables_to_save.append({'failed': 'item not founded',
                                                   'item': item['product_id']})
            self.all_updates['items']: List = [*self.ables_to_save]

    def decrease_quantity_product(self) -> None:
        try:
            for index, item in enumerate(self.ables_to_save):
                new_quantity: int = self.quantities_of_ables_to_save[index] - item['quantity']
                self.product_service.update_one_product_by_id({"_id": item['_id'],
                                                               "quantity": new_quantity})
        except Exception:
            self.decrease_quantity_result: Dict = {'failed': 'An error has occurred'}


class OrdersService(InterfaceEntitiesServices):
    def __init__(self):
        self.database_orders = DB.orders
        self.database_products = ProductsService()
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
            self.__all_orders: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__all_orders: Dict = {'failed': 'An error has occurred'}

    def get_one_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            response: Dict = self.database_orders.find_one({"_id": _id})
            if response:
                self.__order: Dict = response
            else:
                self.__order: Dict = {'failed': 'Order not founded',
                                      '_id': str(_id)}
        except errors.OperationFailure:
            self.__order: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__order: Dict = {'failed': 'An error has occurred'}

    def create_one(self, order: Dict) -> None | Dict:
        """
        Create a single order.

        :param order: Dict = The order requested by client.
        :parameter: order.client_id: str = client ID.
        :parameter: order.items: List[Dict] = List with object items ordered,
         i.e., {'product_id': str, quantity: int}
        :parameter: order.items.product_id: str = product ID.
        :parameter: order.items.quantity: int = quantity ordered.
        :return: Dict
        """
        #  client_id: client ID
        client_id: str = order["client_id"]
        # items: products and theirs quantities
        items: List[Dict] = order['items']
        # instantiate class client that ordered
        order: MakeOrder = MakeOrder(client_id, items)
        # Verify that the client retrieval was successful
        if 'failed' in order.client:
            return {'failed': 'Client not founded',
                    '_id': client_id}
        # set lists products to include or exclude db
        if len(order.ables_to_save) > 0:
            try:
                response: Any = self.database_orders.insert_one(order.get).inserted_id
                if response:
                    # decrease quantity product on stock
                    order.decrease_quantity_product()
                    # Append _id order on orders field on client collection
                    order.client_service.insert_new_order_on_client(str(response))
                    # case exits products to not save, return partial success
                    if len(order.not_ables_to_save) > 0:
                        self.__create_result: Dict = {'success': 'Order partially confirmed',
                                                      '_id': str(response),
                                                      'products_not_included':
                                                          order.not_ables_to_save}
                    # else, absolutely success
                    else:
                        self.__create_result: Dict = {'success': 'Order created',
                                                      '_id': str(response)}
                else:
                    return {'failed': 'An error has occurred'}
            except errors.DuplicateKeyError as error:
                self.__create_result: Dict = {'failed': "Duplicate key error",
                                              'message': error.details.get('keyValue')}
                # Validation field error
            except errors.WriteError as error:
                self.__create_result: Dict = {'failed': "Validate error",
                                              'message': error.details.get('keyValue')}
            except errors.OperationFailure:
                self.__create_result: Dict = {'failed': 'An error has occurred: database operation fails'}
                # generic error
            except Exception:
                self.__create_result: Dict = {'failed': 'An error has occurred'}

        else:
            self.__create_result: Dict = {'failed': 'Any products can be added',
                                          'items': order.not_ables_to_save}

    def update_one_by_id(self, updates: Dict) -> None:
        _id: str = updates["order_id"]
        del updates["order_id"]
        self.get_one_by_id(_id)
        if 'failed' in self.order:
            self.__update_result: Dict = {'failed': 'Order not founded',
                                          '_id': _id}
        else:
            client_id, items, status = Optional[str], Optional[List], Optional[str]
            if 'client_id' in updates:
                client_id: str = updates['client_id']
            if 'items' in updates:
                items: List[Dict] = updates['items']
            if 'status' in updates:
                status: str = updates["status"]
            order: UpdateOrder = UpdateOrder(self.order,
                                             client_id,
                                             items,
                                             status)
            # transactions bellow
            # if exists one or more products to insert
            if len(order.ables_to_save) > 0:
                try:
                    all_updates: Dict = {
                        "$set": order.get
                    }
                    _id: ObjectId = ObjectId(_id)
                    # make req to save
                    response: int = self.database_orders.update_one({'_id': _id},
                                                                    all_updates).modified_count
                    if response > 0:
                        # decrease quantity product on stock
                        order.decrease_quantity_product()
                        # case exits products to not save, return partial success
                        if len(order.not_ables_to_save) > 0:
                            self.__update_result: Dict = {'success': 'Order partially confirmed',
                                                          '_id': str(response),
                                                          'products_not_included':
                                                              order.not_ables_to_save}
                        # else, absolutely success
                        else:
                            self.__update_result: Dict = {'success': 'Updated order',
                                                          'quantity': response}
                    else:
                        self.__update_result: Dict = {'failed': 'An error has occurred'}

                # Exceptions
                # Duplicate key value
                except errors.DuplicateKeyError as error:
                    self.__update_result: Dict = {'failed': "Duplicate key error",
                                                  'message': error.details.get('keyValue')}
                # Validation field error
                except errors.WriteError as error:
                    self.__update_result: Dict = {'failed': "Validate error",
                                                  'message': error.details.get('keyValue')}
                except errors.OperationFailure:
                    self.__update_result: Dict = {'failed': 'An error has occurred: database operation fails'}
                # generic error
                except Exception:
                    self.__update_result: Dict = {'failed': 'An error has occurred'}

            # else, absolutely failed
            else:
                self.__update_result: Dict = {'failed': 'Any items can be modified'}

    def delete_one_by_id(self, _id: str) -> None:
        try:
            # convert str to objectid
            _id: ObjectId = ObjectId(_id)
            # get order saved
            result: Dict = self.database_orders.find_one({"_id": _id})
            # after exclude order, increase quantities in stock
            for item in result['items']:
                self.database_products.get_one_product_by_id(item['_id'], True)
                new_quantity: int = self.database_products.product['quantity'] + item['quantity']
                self.database_products.update_one_product_by_id({"_id": item['_id'],
                                                                 "quantity": new_quantity})
            # exclude
            result: int = self.database_orders.delete_one({"_id": _id}).deleted_count
            self.__delete_result: Dict = {'success': 'Order deleted',
                                          'quantity': result} if \
                result > 0 else {'failed': 'Order not deleted',
                                 '_id': str(_id)}
        except errors.OperationFailure:
            self.__delete_result: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__delete_result: Dict = {'failed': 'An error has occurred'}
