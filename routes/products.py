from typing import Dict, Annotated, List, Union
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, Response, status
from controllers import ProductsController
from models import Product, ProductUpdate, ProductResponse, Failed, Success
from serializers import ProductSerializer
from dependencies import VerifyTokenUser

router: APIRouter = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

controller: ProductsController = ProductsController()


@router.get("/all", response_model=list[ProductResponse] | Failed)
async def get_all_products(verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    result: List[Dict] | Dict = controller.get_all_products()
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_404_NOT_FOUND,
                            media_type="application/json; charset=UTF-8")
    serializer: ProductSerializer = ProductSerializer(result)
    result: List[Dict] = serializer.serialize_all()
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.get("/", response_model=ProductResponse | Failed)
async def get_one_client_by_id(product_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                       title='mongodb _id',
                                                                       description='mongodb _id must be valid'
                                                                       )],
                               verify_token: VerifyTokenUser) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if product_id:
        result: Dict = controller.get_one_product_by_id(product_id)
        if 'failed' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_404_NOT_FOUND,
                                media_type="application/json; charset=UTF-8")
        serializer: ProductSerializer = ProductSerializer(result)
        result: Dict = serializer.serialize_one()
        return JSONResponse(content=result,
                            media_type="application/json; charset=UTF-8")
    result: Dict = {'failed': 'parameter product_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.post("/", response_model=Union[Success, Failed])
async def create_one_product(product: Product,
                             response: Response,
                             verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    product: Dict = product.to_dict()
    result: Dict = controller.create_one_product(product)
    if 'failed' in result:
        if 'message' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_400_BAD_REQUEST,
                                media_type="application/json; charset=UTF-8")
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    response.status_code = status.HTTP_201_CREATED
    return JSONResponse(content=result,
                        media_type="application/json; charset=UTF-8")


@router.put("/", response_model=Union[Success, Failed])
async def update_one_product_by_id(updated: ProductUpdate,
                                   verify_token: VerifyTokenUser) -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    updated: Dict = updated.to_dict()
    result: Dict = controller.update_one_product_by_id(updated)
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
async def delete_one_product_by_id(product_id: Annotated[str | None, Query(regex=r'^[a-f0-9]{24}$',
                                                                           title='mongodb _id',
                                                                           description='mongodb _id must be valid'
                                                                           )],
                                   verify_token: VerifyTokenUser) \
        -> Union[JSONResponse, Dict]:
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if product_id:
        result: Dict = controller.delete_one_product_by_id(product_id)
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
    result: Dict = {'failed': 'parameter product_id must be given'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")
