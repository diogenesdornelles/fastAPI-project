from typing import List, Dict, Annotated, Union, Optional
from fastapi.responses import JSONResponse
from controllers import UsersController
from models import User, UserUpdate, UserResponse, Failed, Success, Data, UserQuery
from fastapi import APIRouter, Query, status
from serializers import UserSerializer
from dependencies import VerifyTokenUser

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

controller: UsersController = UsersController()
serializer: UserSerializer = UserSerializer()


@router.get("/me", response_model=UserResponse | Failed)
async def get_user_me(verify_token: VerifyTokenUser) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if verify_token['user_id']:
        result: Dict = controller.get_one_by_id(verify_token['user_id'])
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
    result: Dict = {'failed': 'parameter user_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.get("/", response_model=UserResponse | Failed)
async def get_one_user_by_id(user_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                  title='mongodb _id',
                                                                  description='mongodb _id must be valid'
                                                                  )],
                             verify_token: VerifyTokenUser

                             ) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if user_id:
        result: Dict = controller.get_one_by_id(user_id)
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
    result: Dict = {'failed': 'parameter user_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.get("/all", response_model=list[UserResponse] | Failed)
async def get_all_users(verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
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
async def get_many_users(verify_token: VerifyTokenUser,
                         name: Optional[str] = None,
                         email: Optional[str] = None,
                         cpf: Optional[str] = None,
                         phone: Optional[str] = None,
                         min_created_at: Optional[Data] = None,
                         max_created_at: Optional[Data] = None,
                         min_last_modified: Optional[Data] = None,
                         max_last_modified: Optional[Data] = None,
                         is_user: Optional[bool] = None):
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    query: UserQuery = UserQuery(**{'name': name,
                                    'email': email,
                                    'cpf': cpf,
                                    'phone': phone,
                                    'min_created_at': min_created_at,
                                    'max_created_at': max_created_at,
                                    'min_last_modified': min_last_modified,
                                    'max_last_modified': max_last_modified,
                                    'is_user': is_user})
    result: Dict = controller.get_many(query)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_404_NOT_FOUND,
                            media_type="application/json; charset=UTF-8")
    result: List[Dict] = serializer.serialize_all(result)
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.post("/", response_model=Union[Success, Failed])
async def create_one_user(user: User) -> Union[JSONResponse, Dict]:
    result: Dict = controller.create_one(user)
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
async def update_one_user_by_id(updates: UserUpdate,
                                verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
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
async def delete_one_user_by_id(user_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                     title='mongodb _id',
                                                                     description='mongodb _id must be valid'
                                                                     )],
                                verify_token: VerifyTokenUser) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if user_id:
        result: Dict = controller.delete_one_by_id(user_id)
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
    result: Dict = {'failed': 'parameter user_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")
