from typing import Optional, List, Dict, Union
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from decimal import Decimal, ROUND_DOWN
import re
from datetime import datetime

PATTERN = r'^[a-f0-9]{24}$'


class Product(BaseModel):
    name: str = Field(min_length=3, description="Product name")
    brand: str = Field(min_length=2, description="Product brand")
    price: Decimal = Field(gt=0, description="Product price")
    description: str = Field(min_length=3, description="Product description")
    quantity: Optional[int] = Field(gt=0, description="Product quantity")

    @validator('price')
    def must_be_float_fixed_two(cls, value) -> float:
        if not isinstance(value, Decimal) or value <= 0:
            raise ValueError('Price must be a positive float value')
        value = value.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        return float(value)

    def to_dict(self):
        return Product.dict(self, exclude_none=True, exclude_unset=True)


class FullProduct(Product):
    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    photos: List = Field(default=[])

    def to_dict(self) -> Dict[str, Union[str, list, datetime, float, int]]:
        return {
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'description': self.description,
            'quantity': self.quantity,
            'created_at': self.created_at,
            'last_modified': self.last_modified,
            'photos': self.photos,
        }


class ProductQuery(BaseModel):
    name: Optional[str] = Field(min_length=3, description="Product name", default=None)
    brand: Optional[str] = Field(min_length=2, description="Product brand", default=None)
    min_price: Optional[float] = Field(gt=0, description="Product price", default=None)
    max_price: Optional[float] = Field(gt=0, description="Product price", default=None)
    description: Optional[str] = Field(min_length=3, description="Product description", default=None)

    def params(self) -> Dict[str, Union[str, float]]:
        params: Dict = {}
        if self.name:
            pattern = re.compile(f".*{self.name}.*", re.IGNORECASE)
            params['name'] = {"$regex": pattern}
        if self.description:
            pattern = re.compile(f".*{self.description}.*", re.IGNORECASE)
            params['description'] = {"$regex": pattern}
        if self.brand:
            pattern = re.compile(self.brand)
            params['brand'] = {"$regex": pattern}
        if self.min_price and self.max_price:
            params['price'] = {"$lt": self.max_price, "$gt": self.min_price}
        elif self.max_price:
            params['price'] = {"$lt": self.max_price}
        elif self.min_price:
            params['price'] = {"$gt": self.min_price}
        return params

    def to_dict(self):
        return ProductQuery.dict(self, exclude_none=True, exclude_unset=True)


class ProductUpdate(BaseModel):
    product_id: str = Field(description="Product ID to update")
    name: Optional[str] = Field(min_length=3, description="Product name")
    brand: Optional[str] = Field(min_length=2, description="Product brand")
    price: Optional[Decimal] = Field(gt=0, description="Product price")
    description: Optional[str] = Field(min_length=3, description="Product description")
    quantity: Optional[int] = Field(gt=0, description="Product quantity")

    @validator('price')
    def must_be_float_fixed_two(cls, value) -> float:
        if not isinstance(value, Decimal) or value <= 0:
            raise ValueError('Price must be a positive float value')
        value = value.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        return float(value)

    @validator('product_id')
    def product_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('product_id must be only numeric, lowercase and length 24')
        return value

    def params(self) -> Dict[str, Union[str, Decimal, ObjectId, int, datetime]]:
        params: Dict[str, Union[str, Decimal, ObjectId, int, datetime]] = {'_id': ObjectId(self.product_id)}
        if self.name:
            params['name'] = self.name
        if self.brand:
            params['brand'] = self.brand
        if self.description:
            params['description'] = self.description
        if self.quantity:
            params['quantity'] = self.quantity
        if self.price:
            params['price'] = self.price
        params['last_modified'] = datetime.now()
        return params


class ProductResponse(BaseModel):
    name: str = Field(min_length=3, description="Product name")
    brand: str = Field(min_length=2, description="Product brand")
    price: float = Field(gt=0, description="Product price")
    description: str = Field(min_length=3, description="Product description")
    quantity: Optional[int] = Field(gt=0, description="Product quantity")
    created_at: str = Field(description="Product create data")
    last_modified: str = Field(description="Product last modified data")
