from typing import Dict, Any

from pydantic import BaseModel, Field, validator


class Failed(BaseModel):
    data: Dict[str, Any] = Field(description='dict must have failed key')

    @validator('data')
    def check_failed_key(cls, value):
        if 'failed' not in value:
            raise ValueError("The 'failed' key must be present in the object.")
        return value
