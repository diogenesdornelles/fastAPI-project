from typing import Dict, List
from utils import convert_objectid_to_str, convert_datetime_to_str


class ProductSerializer:
    def __init__(self):
        self.body = None

    def serialize_all(self, body: Dict | List[Dict]) -> List[Dict]:
        self.body = body
        self.body: List[Dict] = list(self.body)
        self.body: List[Dict] = [convert_objectid_to_str(result) for result in self.body]
        self.body: List[Dict] = [convert_datetime_to_str(result) for result in self.body]
        return self.body

    def serialize_one(self, body: Dict | List[Dict]) -> Dict:
        self.body = body
        self.body: Dict = convert_objectid_to_str(self.body)
        self.body: Dict = convert_datetime_to_str(self.body)
        return self.body
