from datetime import datetime
from typing import Dict


def remove_datetime_fields(obj) -> Dict:
    """
    Remove datetime fiels (created_at and last_modified)
    :param obj - Dict
    :return Dict
    """
    if 'created_at' in obj.keys():
        del obj['created_at']
    if 'last_modified' in obj.keys():
        del obj['last_modified']
    return obj
