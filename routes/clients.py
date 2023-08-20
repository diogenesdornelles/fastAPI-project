from typing import List, Dict, Annotated, Optional, Union
from fastapi.responses import JSONResponse
from fastapi import status
from controllers import ClientsController
from models import Client, ClientUpdate, ClientResponse, Failed, Success, Data, ClientQuery, ClientId
from fastapi import APIRouter, Query
from serializers import ClientSerializer
from dependencies import VerifyTokenUser

router: APIRouter = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

controller: ClientsController = ClientsController()
serializer: ClientSerializer = ClientSerializer()


@router.get("/me", response_model=Union[ClientResponse | Failed])
async def get_client_me(verify_token: VerifyTokenUser) -> JSONResponse | Dict:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if verify_token['client_id']:
        result: Dict = controller.get_one_by_id(verify_token['client_id'])
        if 'failed' in result:
            if '_id' in result:
                return JSONResponse(content=result,
                                    status_code=status.HTTP_404_NOT_FOUND,
                                    media_type="application/json; charset=UTF-8")
            return JSONResponse(content=result,
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                media_type="application/json; charset=UTF-8")
        result: Dict = serializer.serialize_one(result)
        return JSONResponse(content=result,
                            media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter client_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.get("/all", response_model=Union[list[ClientResponse], Failed])
async def get_all_clients(verify_token: VerifyTokenUser) \
        -> JSONResponse | Dict:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: List[Dict] | Dict = controller.get_all()
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")

    result: List[Dict] = serializer.serialize_all(result)
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.get("/many")
async def get_many_clients(verify_token: VerifyTokenUser,
                           name: Optional[str] = None,
                           email: Optional[str] = None,
                           cpf: Optional[str] = None,
                           phone: Optional[str] = None,
                           min_created_at: Optional[Data] = None,
                           max_created_at: Optional[Data] = None,
                           min_last_modified: Optional[Data] = None,
                           max_last_modified: Optional[Data] = None,
                           is_client: Optional[bool] = None):
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    query: ClientQuery = ClientQuery(**{'name': name,
                                        'email': email,
                                        'cpf': cpf,
                                        'phone': phone,
                                        'min_created_at': min_created_at,
                                        'max_created_at': max_created_at,
                                        'min_last_modified': min_last_modified,
                                        'max_last_modified': max_last_modified,
                                        'is_client': is_client})
    result: Dict[str, Union[Data, str, bool]] = controller.get_many(query)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_404_NOT_FOUND,
                            media_type="application/json; charset=UTF-8")
    result: List[Dict] = serializer.serialize_all(result)
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.get("/", response_model=Union[ClientResponse | Failed])
async def get_one_client_by_id(
        verify_token: VerifyTokenUser,
        client_id: ClientId) -> JSONResponse | Dict:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if client_id:
        result: Dict = controller.get_one_by_id(client_id)
        if 'failed' in result:
            if '_id' in result:
                return JSONResponse(content=result,
                                    status_code=status.HTTP_404_NOT_FOUND,
                                    media_type="application/json; charset=UTF-8")
            return JSONResponse(content=result,
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                media_type="application/json; charset=UTF-8")
        result: Dict = serializer.serialize_one(result)
        return JSONResponse(content=result,
                            media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter client_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.post("/", response_model=Union[Success, Failed])
async def create_one_client(verify_token: VerifyTokenUser,
                            client: Client) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: Dict | Failed = controller.create_one(client)
    if 'failed' in result:
        if 'message' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_400_BAD_REQUEST,
                                media_type="application/json; charset=UTF-8")
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    return JSONResponse(content=result,
                        status_code=status.HTTP_201_CREATED,
                        media_type="application/json; charset=UTF-8")


@router.put("/", response_model=Union[Success, Failed])
async def update_one_client_by_id(verify_token: VerifyTokenUser,
                                  updates: ClientUpdate) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: Dict = controller.update_one_by_id(updates)
    if 'failed' in result:
        if 'message' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_400_BAD_REQUEST,
                                media_type="application/json; charset=UTF-8")
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.delete("/", response_model=Union[Success, Failed])
async def delete_one_client_by_id(verify_token: VerifyTokenUser,
                                  client_id: Annotated[Optional[str],
                                  Query(regex=r'^[a-f0-9]{24}$',
                                        title='mongodb _id',
                                        description='mongodb _id must be valid'
                                        )]
                                  ) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if client_id:
        result: Dict = controller.delete_one_by_id(client_id)
        if 'failed' in result:
            if '_id' in result:
                return JSONResponse(content=result,
                                    status_code=status.HTTP_404_NOT_FOUND,
                                    media_type="application/json; charset=UTF-8")
            return JSONResponse(content=result,
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                media_type="application/json; charset=UTF-8")
        return JSONResponse(content=result,
                            media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter client_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")
