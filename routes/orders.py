from typing import List, Dict, Annotated, Union
from fastapi.responses import JSONResponse
from controllers import OrdersController
from fastapi import APIRouter, Query, Depends, Response, status
from models import Order, OrderUpdate, Failed, Success
from serializers import OrderSerializer
from dependencies import token_user_verify

router: APIRouter = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(token_user_verify)],
    responses={404: {"description": "Not found"}},
)

controller: OrdersController = OrdersController()


@router.get("/", response_model=None)
async def get_one_order_by_id(order_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                    title='mongodb _id',
                                                                    description='mongodb _id must be valid'
                                                                    )] = None) \
        -> Union[JSONResponse, Dict]:
    if order_id:
        response: Dict = controller.get_one_order_by_id(order_id)
        serializer: OrderSerializer = OrderSerializer(response)
        response: Dict = serializer.serialize_one()
    else:
        response: Dict = {'failed': 'parameter product_id must be given'}
    return JSONResponse(content=response, media_type="application/json; charset=UTF-8")


@router.get("/all")
async def get_all_orders() -> JSONResponse:
    response: List[Dict] = controller.get_all_orders()
    serializer: OrderSerializer = OrderSerializer(response)
    response: List[Dict] = serializer.serialize_all()
    return JSONResponse(content=response, media_type="application/json; charset=UTF-8")


@router.post("/", response_model=None)
async def create_one_order(order: Order, response: Response) -> Union[JSONResponse, Dict]:
    order: Dict = order.to_dict()
    result: Dict = controller.create_one_order(order)
    response.status_code = status.HTTP_201_CREATED
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.put("/", response_model=None)
async def update_one_order_by_id(updated: OrderUpdate) -> Union[JSONResponse, Dict]:
    order: Dict = updated.to_dict()
    response: Dict = controller.update_one_order_by_id(order)
    return JSONResponse(content=response, media_type="application/json; charset=UTF-8")


@router.delete("/", response_model=None)
async def delete_one_order_by_id(order_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                       title='mongodb _id',
                                                                       description='mongodb _id must be valid'
                                                                       )] = None) \
        -> Union[JSONResponse, Dict]:
    if order_id:
        response: Dict = controller.delete_one_order_by_id(order_id)
    else:
        response: Dict = {'failed': 'parameter product_id must be given'}
    return JSONResponse(content=response, media_type="application/json; charset=UTF-8")
