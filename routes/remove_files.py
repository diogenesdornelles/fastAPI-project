from typing import Annotated, Optional
import os
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from controllers import UploadsController
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

router: APIRouter = APIRouter(
    prefix="/removefiles",
    tags=["removefiles"],
    responses={404: {"description": "Not found"}},
)

controller: UploadsController = UploadsController()

URL_STATIC_PHOTOS_PRODUCTS = os.environ.get("URL_STATIC_PHOTOS_PRODUCTS")

URL_STATIC_PHOTOS_CLIENTS = os.environ.get("URL_STATIC_PHOTOS_CLIENTS")

FILENAME_LENGTH = os.environ.get("FILENAME_LENGTH")

regex_url_photo_client: str = \
    fr'^[{URL_STATIC_PHOTOS_CLIENTS}]{1}/[0-9A-Za-z]{FILENAME_LENGTH}.[png|jpeg|jpg|bmp|tiff]$'

regex_url_photo_product: str = \
    fr'^[{URL_STATIC_PHOTOS_PRODUCTS}]{1}/[0-9A-Za-z]{FILENAME_LENGTH}.[png|jpeg|jpg|bmp|tiff]$'


@router.post("/clients")
async def remove_photo_client(url_file: Annotated[Optional[str], Query(regex=regex_url_photo_client,
                                                                       title='url photo to remove',
                                                                       description='url type must be valid'
                                                                       )],
                              client_id: Annotated[Optional[str], Query(regex=r'^[a-f0-9]{24}$',
                                                                        title='mongodb _id',
                                                                        description='mongodb _id must be valid'
                                                                        )]):
    result = controller.remove_photo_client(url_file, client_id)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    JSONResponse(content=result,
                 media_type="application/json; charset=UTF-8")


@router.post("/products")
async def remove_photo_product(url_file: Annotated[Optional[str], Query(regex=regex_url_photo_product,
                                                                        title='url photo to remove',
                                                                        description='url type must be valid'
                                                                        )],
                               product_id: Annotated[Optional[str], Query(regex=r'^[a-f0-9]{24}$',
                                                                          title='mongodb _id',
                                                                          description='mongodb _id must be valid'
                                                                          )]):
    result = controller.remove_photo_product(url_file, product_id)
    if 'failed' in result:
        return JSONResponse(content=result,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            media_type="application/json; charset=UTF-8")
    JSONResponse(content=result,
                 media_type="application/json; charset=UTF-8")
