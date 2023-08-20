from typing import List, Dict, Any
from bson.objectid import ObjectId
from pymongo import errors
from database import DB
from .interface import IServices, IPhoto
from models import Client, ClientUpdate, FullClient, ClientQuery, ClientId


class ClientsService(IServices, IPhoto):
    def __init__(self):
        self.database = DB.clients
        self.__all_clients = []
        self.__clients = []
        self.__client = {}
        self.__create_result = {}
        self.__update_result = {}
        self.__delete_result = {}
        self.__insert_new_order_result = {}
        self.__insert_new_photo_result = {}
        self.__delete_photo_result = {}

    @property
    def all(self) -> List[Dict]:
        return self.__all_clients

    @property
    def many(self) -> List[Dict]:
        return self.__clients

    @property
    def one(self) -> Dict:
        return self.__client

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
    def insert_new_order_result(self) -> Dict:
        return self.__insert_new_order_result

    @property
    def insert_new_photo_result(self) -> Dict:
        return self.__insert_new_photo_result

    @property
    def delete_photo_result(self) -> Dict:
        return self.__delete_photo_result

    def get_all(self) -> None:
        try:
            response: List[Dict] = self.database.find({},
                                                      {'password': 0})
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_clients: List[Dict] = response
            else:
                self.__all_clients: List = []
        except errors.OperationFailure:
            self.__all_clients: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__all_clients = {'failed': 'An error has occurred'}

    def get_one_by_id(self, _id: ClientId, projection: bool = False) -> None:
        try:
            if projection:
                response: Dict = self.database.find_one({"_id": _id.to_objectid()},
                                                        {'password': 0,
                                                         'orders': 0,
                                                         'created_at': 0,
                                                         'last_modified': 0,
                                                         'photos': 0,
                                                         'is_client': 0})
            else:
                response: Dict = self.database.find_one({"_id": _id.to_objectid()},
                                                        {'password': 0})
            if response:
                self.__client: Dict = response
            else:
                self.__client: Dict = {'failed': 'Client not founded',
                                       '_id': _id.client_id}
        except errors.OperationFailure:
            self.__client: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__client: Dict = {'failed': 'An error has occurred'}

    def get_many(self, query: ClientQuery):
        params: Dict = query.params()
        try:
            response: List[Dict] = self.database.find(params)
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__clients: List[Dict] = response
            else:
                self.__clients: List = []
        except errors.OperationFailure:
            self.__clients: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__clients: Dict = {'failed': 'An error has occurred'}

    def create_one(self, client: Client) -> None:
        client: FullClient = FullClient(**client.to_dict())
        client: Dict = client.to_dict()
        try:
            response: Any = self.database.insert_one(client).inserted_id
            if response:
                self.__create_result: Dict = {'success': 'created client',
                                              '_id': str(response)}
            else:
                self.__create_result: Dict = {'failed': 'client not created'}
        except errors.DuplicateKeyError as error:
            self.__create_result: Dict = {'failed': "duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            print(error)
            self.__create_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except errors.OperationFailure:
            self.__create_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception as error:
            print(error)
            self.__create_result: Dict = {'failed': 'an error has occurred'}

    def update_one_by_id(self, updates: ClientUpdate) -> None:
        updates = updates.params()
        all_updates: Dict = {
            "$set": updates
        }
        try:
            result: int = self.database.update_one({"_id": updates['_id']},
                                                   all_updates).modified_count
            self.__update_result: Dict = {'success': f'{result} client(s) modified'} if result > 0 \
                else {'failed': 'Client not updated',
                      '_id': updates["client_id"]}
        except errors.DuplicateKeyError as error:
            self.__update_result: Dict = {'failed': "duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__update_result: Dict = {'failed': "validate error",
                                          'message': error.details.get('keyValue')}
        except errors.OperationFailure:
            self.__update_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__update_result: Dict = {'failed': 'an error has occurred'}

    def delete_one_by_id(self, client_id: str) -> None:
        client_id: ObjectId = ObjectId(client_id)
        try:
            result: int = self.database.delete_one({"_id": client_id}).deleted_count
            self.__delete_result: Dict = {'success': f'{result} client(s) deleted'} if result > 0 \
                else {'failed': 'client not deleted',
                      '_id': str(client_id)}
        except errors.OperationFailure:
            self.__delete_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__delete_result: Dict = {'failed': 'an error has occurred'}

    def insert_new_order_on_client(self, order_id: str) -> None:
        client_id: ObjectId = ObjectId(self.one['_id'])
        order_id: ObjectId = ObjectId(order_id)
        query: Dict = {
            "_id": client_id
        }
        update: Dict = {
            "$push": {
                "orders": order_id,
            }
        }
        try:
            result: int = self.database.update_one(query, update).modified_count
            self.__insert_new_order_result: Dict = {'success': 'Order inserted',
                                                    'quantity': result}
        except errors.OperationFailure:
            self.__insert_new_order_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__insert_new_order_result: Dict = {'failed': 'an error has occurred'}

    def insert_photo(self, photo_url: str) -> None:
        client_id: ObjectId = ObjectId(self.one['_id'])
        query: Dict = {
            "_id": client_id
        }
        update: Dict = {
            "$push": {
                "photos": photo_url,
            }
        }
        try:
            result: int = self.database.update_one(query, update).modified_count
            self.__insert_new_photo_result: Dict = {'success': 'photo inserted',
                                                    'quantity': result}
        except errors.OperationFailure:
            self.__insert_new_photo_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__insert_new_photo_result: Dict = {'failed': 'an error has occurred'}

    def remove_photo(self, photo_url: str) -> None:
        client_id: ObjectId = ObjectId(self.one['_id'])
        query: Dict = {
            "_id": client_id
        }
        pull: Dict = {
            "$pull": {
                "photos": photo_url
            }
        }
        try:
            result: int = self.database.update_one(query, pull).modified_count
            self.__delete_photo_result: Dict = {'success': 'photo removed',
                                                'quantity': result}
        except errors.OperationFailure:
            self.__delete_photo_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__delete_photo_result: Dict = {'failed': 'an error has occurred'}
