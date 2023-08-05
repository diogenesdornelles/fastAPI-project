from typing import Dict, List
from services import ClientsService
from .interface import IController
from models import Client, ClientUpdate


class ClientsController(IController):
    def __init__(self):
        self.service: ClientsService = ClientsService()

    def get_all(self) -> List[Dict]:
        self.service.get_all()
        response: List[Dict] = self.service.all_clients
        return response

    def get_one_by_id(self, _id: str) -> Dict:
        self.service.get_one_by_id(_id)
        response: Dict = self.service.client
        return response

    def create_one(self, client: Client) -> Dict:
        self.service.create_one(client)
        response: Dict = self.service.create_result
        return response

    def update_one_by_id(self, updates: ClientUpdate) -> Dict:
        self.service.update_one_by_id(updates)
        response: Dict = self.service.update_result
        return response

    def delete_one_by_id(self, _id: str) -> Dict:
        self.service.delete_one_by_id(_id)
        response: Dict = self.service.delete_result
        return response
