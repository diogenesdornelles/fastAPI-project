from typing import Dict
from pymongo.collection import Collection
from pymongo.database import Database

users_validator: Dict = {
    '$jsonSchema': {
        'bsonType': "object",
        'title': "Users Object Validation",
        'required': ["_id",
                     "name",
                     "email",
                     "cpf",
                     "phone",
                     "is_user",
                     "password",
                     "created_at",
                     "last_modified"],
        'additionalProperties': False,
        'properties': {
            "_id": {"bsonType": "objectId"},
            'name': {
                'bsonType': "string",
                'description': "'name' must be a string and is required"
            },
            'email': {
                'bsonType': "string",
                'description': "'email' must be unique, valid and is required",
            },
            'cpf': {
                'bsonType': "string",
                'description': "'cpf' must be unique, valid and is required",
            },
            'password': {
                'bsonType': "string",
                'description': "password is required",
            },
            'phone': {
                'bsonType': "string",
                'description': "'phone' must be valid and is required",
            },
            'is_user': {
                'bsonType': "bool",
                'description': "is_user is required",
            },
            "created_at": {
                'bsonType': "date",
                'description': "Time that created document",
            },
            "last_modified": {
                'bsonType': "date",
                'description': "Time that updated document",
            },
        }
    }
}


def create_users_collection(database: Database) -> Collection:
    users: Collection = database.create_collection('users',
                                                   check_exists=False,
                                                   validator=users_validator
                                                   )
    users.create_index("email", unique=True)
    users.create_index("cpf", unique=True)
    return users
