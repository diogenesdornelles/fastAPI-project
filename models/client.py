from typing import Optional, Dict, List
from pydantic import BaseModel, Field, validator
from utils import CpfValidator
from validate_email import validate_email
import re
from datetime import datetime

PATTERN = r'^[a-f0-9]{24}$'


class Client(BaseModel):
    name: str = Field(min_length=3, description="Client name")
    email: str = Field(description="Client email")
    cpf: str = Field(description="Client cpf")
    phone: str = Field(description="Client phone")
    password: str = Field(description="Client password")
    rep_password: str = Field(description="Client rep. password")

    @validator('cpf')
    def cpf_must_be_valid(cls, value: str) -> str:
        cpf = CpfValidator(value)
        result = cpf.is_valid()
        if not result:
            raise ValueError('CPF must be only numeric and valid')
        return value

    @validator('email')
    def email_must_be_valid(cls, value: str) -> str:
        is_valid = validate_email(value)
        if not is_valid:
            raise ValueError('Email must be valid')
        return value

    @validator('phone')
    def phone_must_be_valid(cls, value: str) -> str:
        if len(value) != 11 or not value.isnumeric():
            raise ValueError('Phone must be only numeric and valid')
        return value

    @validator('password')
    def password_must_be_valid(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password minimum length is 8')
        symbol_cont = 0
        letter_cont = 0
        symbols: str = "!@#$%^&*()_-+={}[]|:;<>,.?/~`"
        for char in value:
            if symbols.count(char) > 0:
                symbol_cont += 1
            if char.isalpha():
                letter_cont += 1
        if symbol_cont < 1:
            raise ValueError('Password must contain at least 1 symbol !@#$%^&*()_'
                             '-+={}[]|:;<>,.?/~`')
        if letter_cont < 1:
            raise ValueError('Password must contain at least 1 letter')
        return value

    @validator('rep_password')
    def passwords_must_match(cls, value: str, values: Dict) -> str:
        if values['password'] != value:
            raise ValueError('Passwords do not match')
        return value

    def to_dict(self) -> Dict:
        return Client.dict(self, exclude_none=True, exclude_unset=True)


class FullClient(Client):
    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    is_client: bool = Field(default=True)
    photos: List = Field(default=[])
    orders: List = Field(default=[])

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'email': self.email,
            'cpf': self.cpf,
            'phone': self.phone,
            'password': self.password,
            'created_at': self.created_at,
            'last_modified': self.last_modified,
            'is_client': self.is_client,
            'photos': self.photos,
            'orders': self.orders
        }


class ClientUpdate(BaseModel):
    client_id: str = Field(min_length=1, description="Client ID to update")
    name: Optional[str] = Field(min_length=3, description="Client name")
    email: Optional[str] = Field(description="Client email")
    cpf: Optional[str] = Field(description="Client cpf")
    phone: Optional[str] = Field(description="Client phone")
    is_client: Optional[bool] = Field(description="Client status")

    @validator('client_id')
    def client_id_must_be_valid(cls, value: str) -> str:
        if not re.match(PATTERN, value):
            raise ValueError('client_id must be only numeric, lowercase and length 24')
        return value

    @validator('cpf')
    def cpf_must_be_valid(cls, value) -> str:
        cpf = CpfValidator(value)
        result = cpf.is_valid()
        if not result:
            raise ValueError('CPF must be only numeric and valid')
        return value

    @validator('email')
    def email_must_be_valid(cls, value) -> str:
        is_valid = validate_email(value)
        if not is_valid:
            raise ValueError('Email must be valid')
        return value

    @validator('phone')
    def phone_must_be_valid(cls, value) -> str:
        if len(value) != 11 or not value.isnumeric():
            raise ValueError('Phone must be only numeric and valid')
        return value

    def to_dict(self):
        return ClientUpdate.dict(self, exclude_none=True, exclude_unset=True)


class ClientAuth(BaseModel):
    password: str = Field(description="Client password")
    email: str = Field(description="Client email")

    @validator('email')
    def email_must_be_valid(cls, value) -> str:
        is_valid = validate_email(value)
        if not is_valid:
            raise ValueError('Email must be valid')
        return value

    @validator('password')
    def password_must_be_valid(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password minimum length is 8')
        symbol_cont = 0
        letter_cont = 0
        symbols: str = "!@#$%^&*()_-+={}[]|:;<>,.?/~`"
        for char in value:
            if symbols.count(char) > 0:
                symbol_cont += 1
            if char.isalpha():
                letter_cont += 1
        if symbol_cont < 1:
            raise ValueError('Password must contain at least 1 symbol !@#$%^&*()_'
                             '-+={}[]|:;<>,.?/~`')
        if letter_cont < 1:
            raise ValueError('Password must contain at least 1 letter')
        return value

    def to_dict(self):
        return ClientAuth.dict(self, exclude_none=True, exclude_unset=True)


class ClientResponse(BaseModel):
    _id: str = Field(min_length=1, description="Client ID to update")
    name: str = Field(min_length=3, description="Client name")
    email: str = Field(description="Client email")
    cpf: str = Field(description="Client cpf")
    phone: str = Field(description="Client phone")
    created_at: str = Field(description="Client creation data")
    last_modified: str = Field(description="Client last update data")
    orders: List[str | None] = Field(description="Client orders _ids")
    is_client: bool = Field(description="Client status")
