from typing import Dict
from fastapi import Request, HTTPException
import jwt
import os
from dotenv import load_dotenv, find_dotenv

from controllers import TokensController

controller = TokensController()

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = os.environ.get("ALGORITHM")


async def token_user_verify(request: Request) -> None:
    bearer_token: str = request.headers.get('authorization')
    if bearer_token:
        try:
            data: str = bearer_token.split(' ')[-1]
            jwt_payload: Dict = jwt.decode(data, key=SECRET_KEY, algorithms=[ALGORITHM])
            token: Dict = jwt_payload['token']
            if 'is_user' not in token or not token['is_user']:
                raise HTTPException(status_code=403, detail="User does not have access rights to the content")
            if not controller.verify_user_token(token['email'], token['password']):
                raise HTTPException(status_code=401, detail="User email not founded "
                                                            "or password is wrong")
            request.state.user = jwt_payload
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail="Invalid token or expired")
    else:
        raise HTTPException(status_code=401, detail="Please, give an authentication token")
