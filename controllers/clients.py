from typing import Dict, List
from services import ClientsService


class ClientsController:
    def __init__(self):
        self.service: ClientsService = ClientsService()

    def get_all_clients(self) -> List[Dict]:
        self.service.get_all_clients()
        response: List[Dict] = self.service.all_clients
        return response

    def get_one_client_by_id(self, _id: str) -> Dict:
        self.service.get_one_client_by_id(_id)
        response: Dict = self.service.client
        return response

    def create_one_client(self, client: Dict):
        self.service.create_one_client(client)
        response: Dict = self.service.create_result
        return response

    def update_one_client_by_id(self, updated: Dict):
        self.service.update_one_client_by_id(updated)
        response: Dict = self.service.update_result
        return response

    def delete_one_client_by_id(self, _id: str) -> Dict:
        self.service.delete_one_client_by_id(_id)
        response: Dict = self.service.delete_result
        return response
