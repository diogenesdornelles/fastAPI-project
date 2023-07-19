from typing import Optional
from pydantic import BaseModel, Field, validator
from decimal import Decimal, ROUND_DOWN
import re

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

    def to_dict(self):
        return ProductUpdate.dict(self, exclude_none=True, exclude_unset=True)


class ProductResponse(BaseModel):
    name: str = Field(min_length=3, description="Product name")
    brand: str = Field(min_length=2, description="Product brand")
    price: float = Field(gt=0, description="Product price")
    description: str = Field(min_length=3, description="Product description")
    quantity: Optional[int] = Field(gt=0, description="Product quantity")
    created_at: str = Field(description="Product create data")
    last_modified: str = Field(description="Product last modified data")
