from typing import Dict
from pymongo.collection import Collection
from pymongo.database import Database

orders_validator: Dict = {
    '$jsonSchema': {
        'bsonType': "object",
        'title': "Products Object Validation",
        'required': ["_id",
                     "client",
                     "items",
                     "status",
                     "created_at",
                     "last_modified"],
        'additionalProperties': False,
        'properties': {
            "_id": {"bsonType": "objectId"},
            "client": {
                'bsonType': "object",
                'title': "Client object validation",
                'required': ["_id",
                             "name",
                             "email",
                             "cpf",
                             "phone"],
                'properties': {
                    "_id": {"bsonType": "string"},
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
                    'phone': {
                        'bsonType': "string",
                        'description': "'phone' must be valid and is required",
                    }
                }
            },
            "items": {
                'bsonType': "array",
                'description': "Products array is required",
                'minItems': 0,
                'items': {
                    'bsonType': "object",
                    'title': "Products Object Validation",
                    'required': ["_id",
                                 "name",
                                 "brand",
                                 "price",
                                 "description",
                                 'quantity'],
                    'properties': {
                        "_id": {"bsonType": "string"},
                        'name': {
                            'bsonType': "string",
                            'description': "'name' must be a string and is required",
                        },
                        'brand': {
                            'bsonType': "string",
                            'description': "'brand' must be string and is required",
                        },
                        'price': {
                            'bsonType': "double",
                            'description': "'price' must be float and is required",
                            'minimum': 0
                        },
                        'description': {
                            'bsonType': "string",
                            'description': "'description' must be string and is required",
                        },
                        "quantity": {
                            'bsonType': "int",
                            'description': "Quantity must be greater than or equal to 1",
                            'minimum': 1,
                        }
                    },
                }
            },
            "status": {
                'enum': ["in_cart",
                         "awaiting_payment",
                         "paid",
                         "shipped",
                         "delivered",
                         "canceled"],
                'description': "Status order is required",
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


def create_orders_collection(database: Database) -> Collection:
    orders: Collection = database.create_collection('orders',
                                                    check_exists=False,
                                                    validator=orders_validator
                                                    )
    return orders
