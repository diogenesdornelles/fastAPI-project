from typing import Dict, Any
from pydantic import BaseModel, Field, validator


class Success(BaseModel):
    data: Dict[str, Any] = Field(description='dict must have success key')

    @validator('data')
    def check_success_key(cls, value):
        if 'failed' not in value:
            raise ValueError("The 'success' key must be present in the object.")
        return value
