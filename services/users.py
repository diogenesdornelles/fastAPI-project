from datetime import datetime
from typing import List, Dict, Any
from bson.objectid import ObjectId
from pymongo import errors
from database import DB
from utils import hash_value


class UsersService:
    def __init__(self):
        self.database = DB.users
        self.__all_users = []
        self.__users = []
        self.__user = {}
        self.__create_result = {}
        self.__update_result = {}
        self.__delete_result = {}

    @property
    def all_users(self) -> List[Dict]:
        return self.__all_users

    @property
    def users(self) -> List[Dict]:
        return self.__users

    @property
    def user(self) -> Dict:
        return self.__user

    @property
    def create_result(self) -> Dict:
        return self.__create_result

    @property
    def update_result(self) -> Dict:
        return self.__update_result

    @property
    def delete_result(self) -> Dict:
        return self.__delete_result

    def get_all_users(self) -> None:
        try:
            response: List[Dict] = self.database.find({},
                                                      {'password': 0})
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_users: List[Dict] = response
            else:
                self.__all_users: List = []
        except Exception:
            self.__all_users: Dict = {'failed': 'An error has occurred'}

    def get_one_user_by_id(self, _id: str) -> None:
        _id = ObjectId(_id)
        try:
            response: Dict = self.database.find_one({"_id": _id},
                                                    {'password': 0})
            if response:
                self.__user: Dict = response
            else:
                self.__user: Dict = {'failed': 'User not founded',
                                     '_id': str(_id)}
        except Exception:
            self.__user = {'failed': 'An error has occurred'}

    def get_users_by_properties(self, properties: Dict, projection: bool = False):
        pass

    def create_one_user(self, user: Dict) -> None:
        user["created_at"]: datetime = datetime.now()
        user["last_modified"]: datetime = datetime.now()
        user['password']: str = hash_value(user['password'])
        user['is_user']: bool = True
        try:
            response: Any = self.database.insert_one(user).inserted_id
            if response:
                self.__create_result: Dict = {'success': 'Created user',
                                              '_id': str(response)}
            else:
                self.__create_result: Dict = {'failed': 'An error has occurred'}
        except errors.DuplicateKeyError as error:
            self.__create_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__create_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except Exception:
            self.__create_result: Dict = {'failed': 'An error has occurred'}

    def update_one_user_by_id(self, updates: Dict) -> None:
        _id: ObjectId = ObjectId(updates["user_id"])
        del updates["user_id"]
        updates["last_modified"]: datetime = datetime.now()
        if 'password' in updates:
            updates['password']: str = hash_value(updates['password'])
        all_updates: Dict = {
            "$set": updates
        }
        try:
            result: int = self.database.update_one({"_id": _id}, all_updates).modified_count
            self.__update_result: Dict = {'success': f'{result} user(s) modified'} if result > 0 \
                else {'failed': 'User not updated',
                      '_id': str(_id)}
        except errors.DuplicateKeyError as error:
            self.__update_result: Dict = {'failed': "Duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__update_result: Dict = {'failed': "Validate error",
                                          'message': error.details.get('keyValue')}
        except Exception:
            self.__update_result: Dict = {'failed': 'An error has occurred'}

    def delete_one_user_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            result: int = self.database.delete_one({"_id": _id}).deleted_count
            self.__delete_result: Dict = {'success': f'{result} user(s) deleted'} if result > 0 \
                else {'failed': 'User not deleted',
                      '_id': str(_id)}
        except Exception:
            self.__delete_result: Dict = {'failed': 'An error has occurred'}
