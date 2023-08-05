from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum
import re

PATTERN = r'^[a-f0-9]{24}$'


class OrderId(BaseModel):
    order_id: str = Field(description="Order ID")

    @validator('order_id')
    def order_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('order_id must be only numeric, lowercase and length 24')
        return value

    def to_str(self):
        return self.order_id


class ClientId(BaseModel):
    client_id: str = Field(description="Client ID")

    @validator('client_id')
    def client_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('client_id must be only numeric, lowercase and length 24')
        return value

    def to_str(self):
        return self.client_id


class ProductId(BaseModel):
    product_id: str = Field(description="product ID")

    @validator('product_id')
    def product_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('product_id must be only numeric, lowercase and length 24')
        return value

    def to_str(self):
        return self.product_id


class Item(BaseModel):
    product_id: ProductId = Field(description="ID product")
    quantity: int = Field(gt=0, description="Quantity product")

    def to_dict(self):
        return Item.dict(self, exclude_none=True, exclude_unset=True)


class OrderStatus(str, Enum):
    IN_CART = 'in_cart'
    AWAITING_PAYMENT = 'awaiting_payment'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class ChangeStatus(BaseModel):
    order_id: OrderId = Field(description="Order id must be valid")
    status: OrderStatus = Field(description="Order status must be valid")

    def to_dict(self):
        return {
            'order_id': self.order_id.to_str(),
            'status': self.status.value()
        }
