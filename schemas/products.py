from typing import Dict
from pymongo.collection import Collection
from pymongo.database import Database

products_validator: Dict = {
    '$jsonSchema': {
        'bsonType': "object",
        'title': "Products Object Validation",
        'required': ["_id",
                     "name",
                     "brand",
                     "price",
                     "description",
                     "photos",
                     "quantity",
                     "created_at",
                     "last_modified"],
        'additionalProperties': False,
        'properties': {
            "_id": {"bsonType": "objectId"},
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
            'quantity': {
                'bsonType': "int",
                'description': "'price' must be integer and is required",
                'minimum': 0,
            },
            'photos': {
                'bsonType': "array",
                'description': "Array of photos url",
                'items': {
                    'bsonType': "string",
                    'description': "Photos url",
                }
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


def create_products_collection(database: Database) -> Collection:
    products: Collection = database.create_collection('products',
                                                      check_exists=False,
                                                      validator=products_validator
                                                      )
    products.create_index("name", unique=True)
    return products
