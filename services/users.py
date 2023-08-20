from typing import List, Dict, Any
from bson.objectid import ObjectId
from pymongo import errors
from database import DB
from .interface import IServices
from models import User, UserUpdate, FullUser, UserQuery


class UsersService(IServices):
    def __init__(self):
        self.database = DB.users
        self.__all_users = []
        self.__users = []
        self.__user = {}
        self.__create_result = {}
        self.__update_result = {}
        self.__delete_result = {}

    @property
    def all(self) -> List[Dict]:
        return self.__all_users

    @property
    def many(self) -> List[Dict]:
        return self.__users

    @property
    def one(self) -> Dict:
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

    def get_all(self) -> None:
        try:
            response: List[Dict] = self.database.find({},
                                                      {'password': 0})
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__all_users: List[Dict] = response
            else:
                self.__all_users: List = []
        except Exception:
            self.__all_users: Dict = {'failed': 'an error has occurred'}

    def get_one_by_id(self, _id: str) -> None:
        _id = ObjectId(_id)
        try:
            response: Dict = self.database.find_one({"_id": _id},
                                                    {'password': 0})
            if response:
                self.__user: Dict = response
            else:
                self.__user: Dict = {'failed': 'user not founded',
                                     '_id': str(_id)}
        except errors.OperationFailure:
            self.__user: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__user = {'failed': 'an error has occurred'}

    def get_many(self, query: UserQuery):
        params: Dict = query.params()
        try:
            response: List[Dict] = self.database.find(params)
            response: List[Dict] = list(response)
            if len(response) > 0:
                self.__users: List[Dict] = response
            else:
                self.__users: List = []
        except errors.OperationFailure:
            self.__users: Dict = {'failed': 'An error has occurred: database operation fails'}
        except Exception:
            self.__users: Dict = {'failed': 'An error has occurred'}

    def create_one(self, user: User) -> None:
        user: FullUser = FullUser(**user.to_dict())
        user: Dict = user.to_dict()
        try:
            response: Any = self.database.insert_one(user).inserted_id
            if response:
                self.__create_result: Dict = {'success': 'created user',
                                              '_id': str(response)}
            else:
                self.__create_result: Dict = {'failed': 'an error has occurred'}
        except errors.DuplicateKeyError as error:
            self.__create_result: Dict = {'failed': "duplicate key error",
                                          'message': error.details.get('keyValue')}
        except errors.WriteError as error:
            self.__create_result: Dict = {'failed': "validate error",
                                          'message': error.details.get('keyValue')}
        except errors.OperationFailure:
            self.__create_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__create_result: Dict = {'failed': 'an error has occurred'}

    def update_one_by_id(self, updates: UserUpdate) -> None:
        updates = updates.params()
        all_updates: Dict = {
            "$set": updates
        }
        try:
            result: int = self.database.update_one({"_id": updates['_id']}, all_updates).modified_count
            self.__update_result: Dict = {'success': f'{result} user(s) modified'} if result > 0 \
                else {'failed': 'User not updated',
                      '_id': str(updates['_id'])}
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

    def delete_one_by_id(self, _id: str) -> None:
        _id: ObjectId = ObjectId(_id)
        try:
            result: int = self.database.delete_one({"_id": _id}).deleted_count
            self.__delete_result: Dict = {'success': f'{result} user(s) deleted'} if result > 0 \
                else {'failed': 'user not deleted',
                      '_id': str(_id)}
        except errors.OperationFailure:
            self.__delete_result: Dict = {'failed': 'an error has occurred: database operation fails'}
        except Exception:
            self.__delete_result: Dict = {'failed': 'an error has occurred'}
