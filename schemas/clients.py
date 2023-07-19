from typing import Dict
from pymongo.collection import Collection
from pymongo.database import Database

clients_validator: Dict = {
    '$jsonSchema': {
        'bsonType': "object",
        'title': "Clients Object Validation",
        'required': ["_id",
                     "name",
                     "email",
                     "cpf",
                     "phone",
                     "orders",
                     "photos",
                     "is_client",
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
            'orders': {
                'bsonType': "array",
                'description': "Array of order objectIds",
                'items': {
                    'bsonType': "objectId",
                    'description': "Refs. a document from orders",
                }
            },
            'photos': {
                'bsonType': "array",
                'description': "Array of photos url",
                'items': {
                    'bsonType': "string",
                    'description': "Photos url",
                }
            },
            'is_client': {
                'bsonType': "bool",
                'description': "is_client is required",
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


def create_clients_collection(database: Database) -> Collection:
    clients: Collection = database.create_collection('clients',
                                                     check_exists=False,
                                                     validator=clients_validator
                                                     )
    clients.create_index("email", unique=True)
    clients.create_index("cpf", unique=True)
    return clients
