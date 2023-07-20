from typing import Dict, Annotated
from fastapi import Request, status, Depends
import jwt
import os
from dotenv import load_dotenv, find_dotenv
from controllers import TokensController

controller = TokensController()

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = os.environ.get("ALGORITHM")


async def token_client_verify(request: Request) -> Dict:
    bearer_token: str = request.headers.get('authorization')
    if bearer_token:
        try:
            data: str = bearer_token.split(' ')[-1]
            jwt_payload: Dict = jwt.decode(data, key=SECRET_KEY, algorithms=[ALGORITHM])
            token: Dict = jwt_payload['token']
            if 'is_client' not in token or not token['is_client']:
                return {'failed': 'User does not have access rights to the content',
                        'status_code': status.HTTP_401_UNAUTHORIZED}
            if not controller.verify_user_token(token['email'], token['password']):
                return {'failed': 'User email not founded or password is wrong',
                        'status_code': status.HTTP_401_UNAUTHORIZED}
            return {'success': 'authentication is ok'}
        except jwt.ExpiredSignatureError:
            return {'failed': 'signature has expired',
                    'status_code': status.HTTP_401_UNAUTHORIZED}
        except jwt.DecodeError:
            return {'failed': 'invalid token',
                    'status_code': status.HTTP_401_UNAUTHORIZED}
    return {'failed': 'give an authentication token',
            'status_code': status.HTTP_401_UNAUTHORIZED}

VerifyTokenClient = Annotated[dict, Depends(token_client_verify)]
