from datetime import datetime
from typing import Dict


def convert_datetime_to_str(obj) -> Dict:
    """
    Converts to str a key from an object if it's value is an instance of datetime
    :param obj - Dict
    :return Dict
    """
    if 'created_at' in obj.keys():
        if isinstance(obj['created_at'], datetime):
            obj["created_at"]: str = obj['created_at'].isoformat()
    if 'last_modified' in obj.keys():
        if isinstance(obj['last_modified'], datetime):
            obj["last_modified"]: str = obj['last_modified'].isoformat()
    return obj
