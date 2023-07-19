from typing import Dict, Annotated, List, Union
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, Depends, Response, status
from controllers import ProductsController
from models import Product, ProductUpdate, ProductResponse, Failed, Success
from serializers import ProductSerializer
from dependencies import token_user_verify

router: APIRouter = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(token_user_verify)],
    responses={404: {"description": "Not found"}},
)

controller: ProductsController = ProductsController()


@router.get("/all", response_model=list[ProductResponse] | Failed)
async def get_all_products(response: Response) -> Union[JSONResponse, Dict]:
    result: List[Dict] | Dict = controller.get_all_products()
    if 'failed' in result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return result
    serializer: ProductSerializer = ProductSerializer(result)
    result: List[Dict] = serializer.serialize_all()
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.get("/", response_model=ProductResponse | Failed)
async def get_one_client_by_id(product_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                       title='mongodb _id',
                                                                       description='mongodb _id must be valid'
                                                                       )],
                               response: Response) \
        -> Union[JSONResponse, Dict]:
    if product_id:
        result: Dict = controller.get_one_product_by_id(product_id)
        if 'failed' in result:
            response.status_code = status.HTTP_404_NOT_FOUND
            return result
        serializer: ProductSerializer = ProductSerializer(result)
        result: Dict = serializer.serialize_one()
        return JSONResponse(content=result, media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter product_id must be given'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return result


@router.post("/", response_model=Union[Success, Failed])
async def create_one_product(product: Product, response: Response) -> Union[JSONResponse, Dict]:
    product: Dict = product.to_dict()
    result: Dict = controller.create_one_product(product)
    if 'failed' in result:
        if 'message' in result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return result
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    response.status_code = status.HTTP_201_CREATED
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.put("/", response_model=Union[Success, Failed])
async def update_one_product_by_id(updated: ProductUpdate, response: Response) -> Union[JSONResponse, Dict]:
    updated: Dict = updated.to_dict()
    result: Dict = controller.update_one_product_by_id(updated)
    if 'failed' in result:
        if 'message' in result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return result
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return result
    return JSONResponse(content=result, media_type="application/json; charset=UTF-8")


@router.delete("/", response_model=Union[Success, Failed])
async def delete_one_product_by_id(product_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                           title='mongodb _id',
                                                                           description='mongodb _id must be valid'
                                                                           )], response: Response) \
        -> Union[JSONResponse, Dict]:
    if product_id:
        result: Dict = controller.delete_one_product_by_id(product_id)
        if 'failed' in result:
            if 'message' in result:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return result
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return result
        return JSONResponse(content=result, media_type="application/json; charset=UTF-8")
    response.status_code = status.HTTP_400_BAD_REQUEST
    result: Dict = {'failed': 'parameter product_id must be given'}
    return result
