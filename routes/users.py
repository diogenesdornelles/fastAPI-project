from typing import List, Dict, Annotated, Union
from fastapi.responses import JSONResponse
from controllers import UsersController
from models import User, UserUpdate, UserResponse, Failed, Success
from fastapi import APIRouter, Query, Depends, Response, status
from serializers import UserSerializer
from dependencies import token_user_verify

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(token_user_verify)],
    responses={404: {"description": "Not found"}},
)

controller = UsersController()


@router.get("/", response_model=UserResponse | Failed)
async def get_one_user_by_id(user_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                  title='mongodb _id',
                                                                  description='mongodb _id must be valid'
                                                                  )], response: Response) \
        -> Union[JSONResponse, Dict]:
    if user_id:
        result: Dict = controller.get_one_user_by_id(user_id)
        if 'failed' in result:
            if '_id' in result:
                response.status_code = status.HTTP_404_NOT_FOUND
                return result
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return result
        serializer: UserSerializer = UserSerializer(result)
        result: Dict = serializer.serialize_one()
        return JSONResponse(content=result, media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter user_id must be given'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.get("/all", response_model=list[UserResponse] | Failed)
async def get_all_users(response: Response) -> Union[JSONResponse, Dict]:
    result: List[Dict] | Dict = controller.get_all_users()
    if 'failed' in result:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    serializer: UserSerializer = UserSerializer(result)
    result: List[Dict] = serializer.serialize_all()
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.post("/", response_model=Union[Success, Failed])
async def create_one_user(user: User, response: Response) -> Union[JSONResponse, Dict]:
    user: Dict = user.to_dict()
    result: Dict = controller.create_one_user(user)
    if 'failed' in result:
        if 'message' in result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return result
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    response.status_code = status.HTTP_201_CREATED
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.put("/", response_model=Union[Success, Failed])
async def update_one_user_by_id(updated: UserUpdate, response: Response) -> Union[JSONResponse, Dict]:
    updated: Dict = updated.to_dict()
    result: Dict = controller.update_one_user_by_id(updated)
    if 'failed' in result:
        if 'message' in result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return result
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.delete("/", response_model=Union[Success, Failed])
async def delete_one_user_by_id(user_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                     title='mongodb _id',
                                                                     description='mongodb _id must be valid'
                                                                     )], response: Response) \
        -> Union[JSONResponse, Dict]:
    if user_id:
        result: Dict = controller.delete_one_user_by_id(user_id)
        if 'failed' in result:
            if '_id' in result:
                response.status_code = status.HTTP_404_NOT_FOUND
                return result
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return result
        return JSONResponse(content=result, media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter user_id must be given'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return result