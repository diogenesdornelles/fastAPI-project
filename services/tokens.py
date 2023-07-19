from typing import Dict
from database import DB
import os
from utils import verify_hashed_value
from dotenv import load_dotenv, find_dotenv
import jwt
from datetime import datetime, timedelta

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = os.environ.get("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


class TokensService:
    def __init__(self):
        self.database_clients = DB.clients
        self.database_users = DB.users

    def create_token_client(self, client: Dict) -> Dict | bool:
        client_saved = self.database_clients.find_one({'email': client['email']},
                                                      {'_id': 0,
                                                       'created_at': 0,
                                                       'last_modified': 0,
                                                       'orders': 0,
                                                       'name': 0,
                                                       'phone': 0,
                                                       'cpf': 0
                                                       })
        if not client_saved:
            return {'failed': 'Client not founded'}
        is_valid = verify_hashed_value(client['password'],
                                       client_saved['password'])
        if is_valid:
            expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            data = {
                'token': client_saved,
                'exp': expiration
            }
            token = jwt.encode(data,
                               key=SECRET_KEY,
                               algorithm=ALGORITHM,
                               json_encoder=None,
                               )
            return {"success": 'created token',
                    "access_token": token,
                    "token_type": "bearer",
                    "expiration": f"{expiration}"}
        return {'failed': 'Passwords not match'}

    def create_token_user(self, user: Dict) -> Dict | bool:
        user_saved = self.database_users.find_one({'email': user['email']},
                                                  {'_id': 0,
                                                   'name': 0,
                                                   'cpf': 0,
                                                   'phone': 0,
                                                   'created_at': 0,
                                                   'last_modified': 0
                                                   })
        if not user_saved:
            return {'failed': 'User not founded'}
        is_valid = verify_hashed_value(user['password'],
                                       user_saved['password'])
        if is_valid:
            expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            data = {
                'token': user_saved,
                'exp': expiration
            }
            token = jwt.encode(data,
                               key=SECRET_KEY,
                               algorithm=ALGORITHM,
                               json_encoder=None,
                               )
            return {"success": 'created token',
                    "access_token": token,
                    "token_type": "bearer",
                    "expiration": f"{expiration}"}
        return {'failed': 'Passwords not match'}

    def verify_client_token(self, email: str, password: str) -> bool:
        client_saved = self.database_clients.find_one({'email': email})
        if not client_saved:
            return False
        return password == client_saved['password']

    def verify_user_token(self, email: str, password: str) -> bool:
        user_saved = self.database_users.find_one({'email': email})
        if not user_saved:
            return False
        return password == user_saved['password']
