from typing import Optional, Dict
import re
from utils import CpfValidator
from validate_email import validate_email
from pydantic import BaseModel, Field, validator
from models import Client, ClientAuth

PATTERN = r'^[a-f0-9]{24}$'


class User(BaseModel):
    name: str = Field(min_length=3, description="User name")
    email: str = Field(description="User email")
    cpf: str = Field(description="User cpf")
    phone: str = Field(description="User phone")
    password: str = Field(description="User password")
    rep_password: str = Field(description="User rep. password")

    @validator('cpf')
    def cpf_must_be_valid(cls, value: str):
        cpf = CpfValidator(value)
        result = cpf.is_valid()
        if not result:
            raise ValueError('CPF must be only numeric and valid')
        return value

    @validator('email')
    def email_must_be_valid(cls, value: str):
        is_valid = validate_email(value)
        if not is_valid:
            raise ValueError('Email must be valid')
        return value

    @validator('phone')
    def phone_must_be_valid(cls, value: str):
        if len(value) != 11 or not value.isnumeric():
            raise ValueError('Phone must be only numeric and valid')
        return value

    @validator('password')
    def password_must_be_valid(cls, value: str):
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
    def passwords_must_match(cls, value: str, values: Dict):
        if values['password'] != value:
            raise ValueError('Passwords do not match')
        return value

    def to_dict(self):
        del self.rep_password
        return Client.dict(self, exclude_none=True, exclude_unset=True)


class UserUpdate(BaseModel):
    user_id: str = Field(min_length=1, description="Client ID to update")
    name: Optional[str] = Field(min_length=3, description="Client name")
    email: Optional[str] = Field(description="Client email")
    cpf: Optional[str] = Field(description="Client cpf")
    phone: Optional[str] = Field(description="Client phone")
    is_user: Optional[bool] = Field(description="Client status")

    @validator('user_id')
    def user_id_must_be_valid(cls, value: str):
        if not re.match(PATTERN, value):
            raise ValueError('user_id must be only numeric, lowercase and length 24')
        return value

    @validator('cpf')
    def cpf_must_be_valid(cls, value):
        cpf = CpfValidator(value)
        result = cpf.is_valid()
        if not result:
            raise ValueError('CPF must be only numeric and valid')
        return value

    @validator('email')
    def email_must_be_valid(cls, value):
        is_valid = validate_email(value)
        if not is_valid:
            raise ValueError('Email must be valid')
        return value

    @validator('phone')
    def phone_must_be_valid(cls, value):
        if len(value) != 11 or not value.isnumeric():
            raise ValueError('Phone must be only numeric and valid')
        return value

    def to_dict(self):
        return UserUpdate.dict(self, exclude_none=True, exclude_unset=True)


class UserAuth(ClientAuth):
    pass


class UserResponse(BaseModel):
    _id: str = Field(min_length=1, description="User ID to update")
    name: str = Field(min_length=3, description="User name")
    email: str = Field(description="User email")
    cpf: str = Field(description="User cpf")
    phone: str = Field(description="User phone")
    created_at: str = Field(description="User creation data")
    last_modified: str = Field(description="User last update data")
    is_user: bool = Field(description="User status")
