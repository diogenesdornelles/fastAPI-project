from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
import re

PATTERN = r'^[a-f0-9]{24}$'


class Item(BaseModel):
    product_id: str = Field(description="IDs products")
    quantity: int = Field(gt=0, description="Quantity products")

    def to_dict(self):
        return Item.dict(self, exclude_none=True, exclude_unset=True)

    @validator('product_id')
    def product_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('product_id must be only numeric, lowercase and length 24')
        return value


class OrderStatus(str, Enum):
    IN_CART = 'in_cart'
    AWAITING_PAYMENT = 'awaiting_payment'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class Order(BaseModel):
    client_id: str = Field(description="Client ID")
    items: List[Item] = Field(description="Products list")

    @validator('client_id')
    def client_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('client_id must be only numeric, lowercase and length 24')
        return value

    @validator('items')
    def validate_items_length(cls, array):
        if len(array) < 1:
            raise ValueError('Items must have a minimum length of 1')
        return array

    def to_dict(self):
        products: List = []
        for item in self.items[:]:
            products.append(item.to_dict())
        self.items = products
        return Item.dict(self, exclude_none=True, exclude_unset=True)


class OrderUpdate(BaseModel):
    order_id: str = Field(description="Order ID to update")
    client_id: Optional[str] = Field(description="ID client")
    items: Optional[List[Item]] = Field(description="Products list")
    status: Optional[OrderStatus] = Field(description="Order status")

    @validator('client_id')
    def client_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('client_id must be only numeric, lowercase and length 24')
        return value

    @validator('order_id')
    def order_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('order_id must be only numeric, lowercase and length 24')
        return value

    @validator('items')
    def validate_items_length(cls, array):
        if len(array) < 1:
            raise ValueError('Items must have a minimum length of 1')
        return array

    def to_dict(self):
        products: List = []
        for item in self.items[:]:
            products.append(item.to_dict())
        self.items = products
        return Item.dict(self, exclude_none=True, exclude_unset=True)
