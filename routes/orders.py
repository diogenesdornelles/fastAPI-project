from typing import List, Dict, Annotated, Union
from fastapi.responses import JSONResponse
from controllers import OrdersController
from fastapi import APIRouter, Query, status
from models import ClientId, Failed, Success, ChangeStatus, Item, ProductId
from serializers import OrderSerializer
from dependencies import VerifyTokenUser

router: APIRouter = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

controller: OrdersController = OrdersController()
serializer: OrderSerializer = OrderSerializer()


@router.get("/", response_model=None)
async def get_one_order_by_id(order_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                    title='mongodb _id',
                                                                    description='mongodb _id must be valid'
                                                                    )],
                              verify_token: VerifyTokenUser) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if order_id:
        result: Dict = controller.get_one_by_id(order_id)
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
    result: Dict = {'failed': 'parameter order_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.get("/all")
async def get_all_orders(verify_token: VerifyTokenUser) -> JSONResponse:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: List[Dict] = controller.get_all()
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    result: List[Dict] = serializer.serialize_all(result)
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.post("/", response_model=Union[Success, Failed])
async def create_one_order(client_id: ClientId,
                           verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    client_id: Dict = client_id.to_str()
    result: Dict = controller.create_one(client_id)
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


# @router.put("/", response_model=Union[Success, Failed])
# async def update_one_order_by_id(updated: OrderUpdate,
#                                  verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
#     if 'failed' in verify_token:
#         return JSONResponse(content=verify_token,
#                             status_code=verify_token['status_code'],
#                             media_type="application/json; charset=UTF-8")
#     order: Dict = updated.to_dict()
#     result: Dict = controller.update_one_by_id(order)
#     if 'failed' in result:
#         if 'message' in result:
#             return JSONResponse(content=result,
#                                 status_code=status.HTTP_400_BAD_REQUEST,
#                                 media_type="application/json; charset=UTF-8")
#         return JSONResponse(content=result,
#                             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             media_type="application/json; charset=UTF-8")
#     return JSONResponse(content=result,
#                         media_type="application/json; charset=UTF-8")


@router.put("/add/{order_id}", response_model=Union[Success, Failed])
async def add_item(item: Item,
                   order_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                         title='mongodb _id',
                                                         description='mongodb _id must be valid'
                                                         )],
                   verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: Dict = controller.add_item(order_id, item)
    if 'failed' in result:
        if '_id' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_400_BAD_REQUEST,
                                media_type="application/json; charset=UTF-8")
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.put("/remove/{order_id}", response_model=Union[Success, Failed])
async def remove_item(product_id: ProductId,
                      order_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                            title='mongodb _id',
                                                            description='mongodb _id must be valid'
                                                            )],
                      verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    product_id: str = product_id.to_str()
    result: Dict = controller.remove_item(order_id, product_id)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.put("/", response_model=Union[Success, Failed])
async def change_status(cart_status: ChangeStatus,
                        verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: Dict = controller.change_status(cart_status)


@router.delete("/", response_model=Union[Success, Failed])
async def delete_one_order_by_id(order_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                       title='mongodb _id',
                                                                       description='mongodb _id must be valid'
                                                                       )],
                                 verify_token: VerifyTokenUser) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if order_id:
        result: Dict = controller.delete_one_by_id(order_id)
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
