from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Dict, List
from enum import Enum
import re

PATTERN = r'^[a-f0-9]{24}$'


class OrderId(BaseModel):
    order_id: str = Field(description="Order ID")

    @validator('order_id')
    def order_id_must_be_valid(cls, value: str) -> str:
        if not re.match(PATTERN, value):
            raise ValueError('order_id must be only numeric, lowercase and length 24')
        return value

    def to_objectid(self) -> ObjectId:
        return ObjectId(self.order_id)


class ClientId(BaseModel):
    client_id: str = Field(description="Client ID")

    @validator('client_id')
    def client_id_must_be_valid(cls, value: str) -> str:
        if not re.match(PATTERN, value):
            raise ValueError('client_id must be only numeric, lowercase and length 24')
        return value

    def to_objectid(self) -> ObjectId:
        return ObjectId(self.client_id)


class ProductId(BaseModel):
    product_id: str = Field(description="product ID")

    @validator('product_id')
    def product_id_must_be_valid(cls, value: str) -> str:
        if not re.match(PATTERN, value):
            raise ValueError('product_id must be only numeric, lowercase and length 24')
        return value

    def to_objectid(self) -> ObjectId:
        return ObjectId(self.product_id)


class AddItem(OrderId, ProductId):
    quantity: int = Field(gt=0, description="Quantity product")

    def to_dict(self) -> Dict:
        return AddItem.dict(self, exclude_none=True, exclude_unset=True)

    def get_orderid(self) -> OrderId:
        return OrderId(**{
            'order_id': self.order_id
        })

    def get_productid(self) -> ProductId:
        return ProductId(**{
            'product_id': self.product_id
        })


class RemoveItem(OrderId, ProductId):
    def to_dict(self) -> Dict:
        return RemoveItem.dict(self, exclude_none=True, exclude_unset=True)

    def get_orderid(self) -> OrderId:
        return OrderId(**{
            'order_id': self.order_id
        })

    def get_productid(self) -> ProductId:
        return ProductId(**{
            'product_id': self.product_id
        })


class OrderStatus(str, Enum):
    IN_CART = 'in_cart'
    AWAITING_PAYMENT = 'awaiting_payment'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class ChangeStatus(OrderId):
    status: OrderStatus = Field(description="Order status must be valid")

    def to_dict(self) -> Dict:
        return {
            'order_id': self.order_id,
            'status': self.status.value()
        }

    def get_orderid(self) -> OrderId:
        return OrderId(**{
            'order_id': self.order_id
        })


class FullOrder(BaseModel):
    client: Dict = Field(description="Client")
    status: str = Field(description="Status", default='in_cart')
    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    items: List[None] = Field(default=[])

    def to_dict(self) -> Dict:
        return RemoveItem.dict(self, exclude_none=True, exclude_unset=True)
