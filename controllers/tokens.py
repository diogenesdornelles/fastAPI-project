from typing import Dict
from services import TokensService


class TokensController:
    def __init__(self):
        self.service: TokensService = TokensService()

    def create_token_client(self, client: Dict) -> Dict:
        response: Dict = self.service.create_token_client(client)
        return response

    def create_token_user(self, user: Dict) -> Dict:
        response: Dict = self.service.create_token_user(user)
        return response

    def verify_user_token(self, email: str, password: str) -> bool:
        response: bool = self.service.verify_user_token(email, password)
        return response

    def verify_client_token(self, email: str, password: str) -> bool:
        response: bool = self.service.verify_client_token(email, password)
        return response
