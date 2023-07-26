from typing import Dict
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from models import ClientAuth, UserAuth
from controllers import TokensController
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = os.environ.get("ALGORITHM")

router: APIRouter = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

controller: TokensController = TokensController()


@router.post("/clients", response_model=None)
async def create_token_client(client: ClientAuth) -> JSONResponse:
    client: Dict = client.to_dict()
    result: Dict = controller.create_token_client(client)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_400_BAD_REQUEST,
                            media_type="application/json; charset=UTF-8")
    return JSONResponse(content=result,
                        status_code=status.HTTP_201_CREATED,
                        media_type="application/json; charset=UTF-8")


@router.post("/users", response_model=None)
async def create_token_client(user: UserAuth) -> JSONResponse:
    user: Dict = user.to_dict()
    result: Dict = controller.create_token_user(user)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_400_BAD_REQUEST,
                            media_type="application/json; charset=UTF-8")
    return JSONResponse(content=result,
                        status_code=status.HTTP_201_CREATED,
                        media_type="application/json; charset=UTF-8")
