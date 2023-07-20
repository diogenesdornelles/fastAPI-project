from typing import Annotated, Optional, Dict
import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, Query, status
from fastapi.responses import JSONResponse
from utils import generate_random_string
from controllers import UploadsController
from dotenv import load_dotenv, find_dotenv
from dependencies import VerifyTokenUser

load_dotenv(find_dotenv())

controller: UploadsController = UploadsController()

router: APIRouter = APIRouter(
    prefix="/uploadfiles",
    tags=["uploadfiles"],
    responses={404: {"description": "Not found"}},
)

URL_STATIC_PHOTOS_PRODUCTS = os.environ.get("URL_STATIC_PHOTOS_PRODUCTS")

URL_STATIC_PHOTOS_CLIENTS = os.environ.get("URL_STATIC_PHOTOS_CLIENTS")

FILENAME_LENGTH = os.environ.get("FILENAME_LENGTH")


@router.post("/clients")
async def upload_photo_client(file: UploadFile,
                              client_id: Annotated[Optional[str], Query(regex=r'^[a-f0-9]{24}$',
                                                                        title='mongodb _id',
                                                                        description='mongodb _id must be valid'
                                                                        )],
                              verify_token: VerifyTokenUser):
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if 'image' in file.content_type:
        current_dir: str = os.getcwd()
        static_dir_clients: str = os.path.join(current_dir,
                                               'static',
                                               'clients',
                                               'photos')
        os.makedirs(static_dir_clients, exist_ok=True)
        target_dir: Path = Path(static_dir_clients)
        ext: str = file.filename.split('.')[-1]
        random_name: str = generate_random_string(FILENAME_LENGTH)
        filename: str = f'{random_name}.{ext}'
        target_path: Path = target_dir / filename
        result: Dict = controller.upload_photo_client(client_id,
                                                      f'{URL_STATIC_PHOTOS_CLIENTS}/{filename}')
        if 'failed' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                media_type="application/json; charset=UTF-8")
        with target_path.open("wb") as destination:
            while chunk := await file.read(1024):
                destination.write(chunk)
        return JSONResponse(content=result,
                            status_code=status.HTTP_201_CREATED,
                            media_type="application/json; charset=UTF-8")
    result = {'failed': 'only image files are supported'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")


@router.post("/products")
async def upload_photo_product(file: UploadFile,
                               product_id: Annotated[Optional[str], Query(regex=r'^[a-f0-9]{24}$',
                                                                          title='mongodb _id',
                                                                          description='mongodb _id must be valid'
                                                                          )],
                               verify_token: VerifyTokenUser):
    if 'failed' in verify_token:
        return JSONResponse(content=verify_token,
                            status_code=verify_token['status_code'],
                            media_type="application/json; charset=UTF-8")
    if 'image' in file.content_type:
        current_dir: str = os.getcwd()
        static_dir_products: str = os.path.join(current_dir, 'static', 'products', 'photos')
        os.makedirs(static_dir_products, exist_ok=True)
        target_dir: Path = Path(static_dir_products)
        ext: str = file.filename.split('.')[-1]
        random_name: str = generate_random_string(24)
        filename: str = f'{random_name}.{ext}'
        target_path: Path = target_dir / filename
        result: Dict = controller.upload_photo_product(product_id,
                                                       f'{URL_STATIC_PHOTOS_PRODUCTS}/{filename}')
        if 'failed' in result:
            return JSONResponse(content=result,
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                media_type="application/json; charset=UTF-8")
        with target_path.open("wb") as destination:
            while chunk := await file.read(1024):
                destination.write(chunk)
        return JSONResponse(content=result,
                            status_code=status.HTTP_201_CREATED,
                            media_type="application/json; charset=UTF-8")
    result = {'failed': 'only image files are supported'}
    return JSONResponse(content=result,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        media_type="application/json; charset=UTF-8")
