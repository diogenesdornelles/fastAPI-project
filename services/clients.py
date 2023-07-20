from datetime import datetime
from typing import List, Dict, Any
from bson.objectid import ObjectId
from pymongo import errors
from database import DB
from utils import hash_value


class ClientsService:
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
    def all_clients(self) -> List[Dict]:
        return self.__all_clients

    @property
    def clients(self) -> List[Dict]:
        return self.__clients

    @property
    def client(self) -> Dict:
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

    def get_all_clients(self) -> None:
        try:
            response: List[Dict] = self.database.find({},
                                                      {'password': 0})
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_clients: List[Dict] = response
            else:
                self.__all_clients: List = []
        except Exception:
            self.__all_clients = {'failed': 'An error has occurred'}

    def get_one_client_by_id(self, _id: str, projection: bool = False) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            if projection:
                response: Dict = self.database.find_one({"_id": _id},
                                                        {'password': 0,
                                                         'orders': 0,
                                                         'created_at': 0,
                                                         'last_modified': 0})
            else:
                response: Dict = self.database.find_one({"_id": _id},
                                                        {'password': 0})
            if response:
                self.__client: Dict = response
            else:
                self.__client: Dict = {'failed': 'Client not founded',
                                       '_id': _id}
        except Exception:
            self.__client: Dict = {'failed': 'An error has occurred'}

    def get_clients_by_properties(self, properties: Dict, projection: bool = False):
        pass

    def create_one_client(self, client: Dict) -> None:
        client["created_at"]: datetime = datetime.now()
        client["last_modified"]: datetime = datetime.now()
        client["orders"]: List = []
        client["photos"]: List = []
        client['password']: str = hash_value(client['password'])
        client['is_client']: bool = True
        try:
            response: Any = self.database.insert_one(client).inserted_id
            if response:
                self.__create_result: Dict = {'success': 'Created client',
                                              '_id': str(response)}
            else:
                self.__create_result: Dict = {'failed': 'Client not created'}
        except errors.DuplicateKeyError as error:
            self.__create_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__create_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except Exception:
            self.__create_result: Dict = {'failed': 'An error has occurred'}

    def update_one_client_by_id(self, updates: Dict) -> None:
        _id: ObjectId = ObjectId(updates["client_id"])
        if 'photos' in updates:
            del updates['photos']
        del updates["client_id"]
        updates["last_modified"]: datetime = datetime.now()
        if 'password' in updates:
            updates['password']: str = hash_value(updates['password'])
        all_updates: Dict = {
            "$set": updates
        }
        try:
            result: int = self.database.update_one({"_id": _id},
                                                   all_updates).modified_count
            self.__update_result: Dict = {'success': f'{result} client(s) modified'} if result > 0 \
                else {'failed': 'Client not updated',
                      '_id': updates["client_id"]}
        except errors.DuplicateKeyError as error:
            self.__update_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__update_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except Exception:
            self.__update_result: Dict = {'failed': 'An error has occurred'}

    def delete_one_client_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            result: int = self.database.delete_one({"_id": _id}).deleted_count
            self.__delete_result: Dict = {'success': f'{result} client(s) deleted'} if result > 0 \
                else {'failed': 'Client not deleted',
                      '_id': str(_id)}
        except Exception:
            self.__delete_result: Dict = {'failed': 'An error has occurred'}

    def insert_new_order_on_client(self, order_id: str) -> None:
        client_id: ObjectId = ObjectId(self.client['_id'])
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
        except Exception:
            self.__insert_new_order_result: Dict = {'failed': 'An error has occurred'}

    def insert_new_photo_on_client(self, photo_url: str) -> None:
        client_id: ObjectId = ObjectId(self.client['_id'])
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
            self.__insert_new_photo_result: Dict = {'success': 'Photo inserted',
                                                    'quantity': result}
        except Exception:
            self.__insert_new_photo_result: Dict = {'failed': 'An error has occurred'}

    def remove_photo_from_client(self, photo_url: str) -> None:
        client_id: ObjectId = ObjectId(self.client['_id'])
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
            self.__insert_new_photo_result: Dict = {'success': 'Photo removed',
                                                    'quantity': result}
        except Exception:
            self.__delete_photo_result: Dict = {'failed': 'An error has occurred'}
