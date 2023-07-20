from typing import Dict
from bson.objectid import ObjectId


def convert_objectid_to_str(obj: Dict) -> Dict:
    """
    Converts a key from an object if it's value is an instance of ObjectId
    :param obj - Dict
    :return Dict
    """
    if isinstance(obj['_id'], ObjectId):
        obj["_id"] = str(ObjectId(obj['_id']))
    return obj
