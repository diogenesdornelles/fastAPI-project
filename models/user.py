from typing import Optional, Dict, Union, Any
import re

from bson import ObjectId

from utils import CpfValidator, hash_value
from validate_email import validate_email
from pydantic import BaseModel, Field, validator
from models import ClientAuth
from .data import Data
from datetime import datetime

PATTERN = r'^[a-f0-9]{24}$'


class User(BaseModel):
    name: str = Field(min_length=3, description="User name")
    email: str = Field(description="User email")
    cpf: str = Field(description="User cpf")
    phone: str = Field(description="User phone")
    password: str = Field(description="User password")
    rep_password: str = Field(description="User rep. password")

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
        return User.dict(self, exclude_none=True, exclude_unset=True)


class FullUser(User):
    created_at: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    is_user: bool = Field(default=True)

    def to_dict(self) -> Dict[str, Union[str, datetime, bool]]:
        return {
            'name': self.name,
            'email': self.email,
            'cpf': self.cpf,
            'phone': self.phone,
            'password': hash_value(self.password),
            'created_at': self.created_at,
            'last_modified': self.last_modified,
            'is_user': self.is_user
        }


class UserQuery(User):
    name: Optional[str] = Field(min_length=3, description="User name", default=None)
    email: Optional[str] = Field(description="User email", default=None)
    cpf: Optional[str] = Field(description="User cpf", default=None)
    phone: Optional[str] = Field(description="User phone", default=None)
    min_created_at: Optional[Data] = Field(description="User minimum data creation", default=None)
    max_created_at: Optional[Data] = Field(description="User maximum data creation", default=None)
    min_last_modified: Optional[Data] = Field(description="User minimum data modification", default=None)
    max_last_modified: Optional[Data] = Field(description="User maximum data modification", default=None)
    is_user: Optional[bool] = Field(description="User status", default=None)
    password: Optional[str] = Field(description="User password", default=None)
    rep_password: Optional[str] = Field(description="User rep. password", default=None)

    def params(self) -> Dict[str, Dict[str, Any]]:
        params: Dict = {}
        if self.name:
            pattern = re.compile(f".*{self.name}.*", re.IGNORECASE)
            params['name'] = {"$regex": pattern}
        if self.cpf:
            pattern = re.compile(f".*{self.cpf}.*", re.IGNORECASE)
            params['cpf'] = {"$regex": pattern}
        if self.phone:
            pattern = re.compile(f".*{self.phone}.*", re.IGNORECASE)
            params['phone'] = {"$regex": pattern}
        if self.email:
            pattern = re.compile(f".*{self.email}.*", re.IGNORECASE)
            params['email'] = {"$regex": pattern}
        if self.is_user:
            params['is_user'] = self.is_user
        if self.min_created_at and self.max_created_at:
            params['created_at'] = {"$lt": self.max_created_at, "$gt": self.min_created_at}
        elif self.max_created_at:
            params['created_at'] = {"$lt": self.max_created_at}
        elif self.min_created_at:
            params['created_at'] = {"$gt": self.min_created_at}
        if self.min_last_modified and self.max_last_modified:
            params['last_modified'] = {"$lt": self.max_last_modified, "$gt": self.min_last_modified}
        elif self.max_created_at:
            params['last_modified'] = {"$lt": self.max_last_modified}
        elif self.min_created_at:
            params['last_modified'] = {"$gt": self.min_last_modified}
        return params

    @validator('password')
    def password_must_be_valid(cls, value: str) -> None:
        return None

    @validator('rep_password')
    def passwords_must_match(cls, value: str, values: Dict) -> None:
        return None


class UserUpdate(User):
    user_id: str = Field(min_length=1, description="User ID to update")
    name: Optional[str] = Field(min_length=3, description="User new name")
    email: Optional[str] = Field(description="User new email")
    cpf: Optional[str] = Field(description="User new cpf")
    phone: Optional[str] = Field(description="User new phone")
    is_user: Optional[bool] = Field(description="User new status")
    password: Optional[str] = Field(description="User password", exclude=True)
    rep_password: Optional[str] = Field(description="User rep. password", exclude=True)

    @validator('user_id')
    def user_id_must_be_valid(cls, value: str) -> str:
        if not re.match(PATTERN, value):
            raise ValueError('user_id must be only numeric, lowercase and length 24')
        return value

    def params(self) -> Dict[str, Union[str, bool, ObjectId, datetime]]:
        params: Dict[str, Union[str, bool, ObjectId, datetime]] = {'_id': ObjectId(self.user_id)}
        if self.name:
            params['name'] = self.name
        if self.cpf:
            params['cpf'] = self.cpf
        if self.email:
            params['email'] = self.email
        if self.phone:
            params['phone'] = self.phone
        if self.password:
            params['password'] = hash_value(self.password)
        if self.is_user:
            params['is_client'] = self.is_user
        params['last_modified'] = datetime.now()
        return params


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
