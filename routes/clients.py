from typing import List, Dict, Annotated, Optional, Union
from fastapi.responses import JSONResponse
from fastapi import Response, status, Depends
from controllers import ClientsController
from models import Client, ClientUpdate, ClientResponse, Failed, Success
from fastapi import APIRouter, Query
from serializers import ClientSerializer
from dependencies import token_user_verify

router: APIRouter = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(token_user_verify)],
    responses={404: {"description": "Not found"}},
)

controller = ClientsController()


@router.get("/all", response_model=Union[list[ClientResponse], Failed])
async def get_all_clients(response: Response) -> JSONResponse | Dict:
    result: List[Dict] | Dict = controller.get_all_clients()
    if 'failed' in result:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    serializer: ClientSerializer = ClientSerializer(result)
    result: List[Dict] = serializer.serialize_all()
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.get("/", response_model=Union[ClientResponse | Failed])
async def get_one_client_by_id(
        client_id: Annotated[Optional[str], Query(regex=r'^[a-f0-9]{24}$',
                                                  title='mongodb _id',
                                                  description='mongodb _id must be valid'
                                                  )],
        response: Response
) -> JSONResponse | Dict:
    if client_id:
        result: Dict = controller.get_one_client_by_id(client_id)
        if 'failed' in result:
            if '_id' in result:
                response.status_code = status.HTTP_404_NOT_FOUND
                return result
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return result
        serializer: ClientSerializer = ClientSerializer(result)
        result: Dict = serializer.serialize_one()
        return JSONResponse(content=result, media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter client_id must be given'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.post("/", response_model=Union[Success, Failed])
async def create_one_client(client: Client, response: Response) -> Union[JSONResponse, Dict]:
    client: Dict = client.to_dict()
    result: Dict | Failed = controller.create_one_client(client)
    if 'failed' in result:
        if 'message' in result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return result
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    response.status_code = status.HTTP_201_CREATED
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.put("/", response_model=Union[Success, Failed])
async def update_one_client_by_id(updated: ClientUpdate, response: Response) -> Union[JSONResponse, Dict]:
    updated: Dict = updated.to_dict()
    result: Dict = controller.update_one_client_by_id(updated)
    if 'failed' in result:
        if 'message' in result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return result
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.delete("/", response_model=Union[Success, Failed])
async def delete_one_client_by_id(client_id: Annotated[Optional[str], Query(regex=r'^[a-f0-9]{24}$',
                                                                            title='mongodb _id',
                                                                            description='mongodb _id must be valid'
                                                                            )],
                                  response: Response
                                  ) -> Union[JSONResponse, Dict]:
    if client_id:
        result: Dict = controller.delete_one_client_by_id(client_id)
        if 'failed' in result:
            if '_id' in result:
                response.status_code = status.HTTP_404_NOT_FOUND
                return result
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return result
        return JSONResponse(content=result, media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter client_id must be given'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return result
