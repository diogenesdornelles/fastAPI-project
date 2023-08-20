from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator, Field


class Data(BaseModel):
    data: Optional[str] = Field(min_length=10, description="data pt-br")

    @validator('data')
    def is_valid(cls, value: str) -> datetime:
        day, month, year = value.split('/')
        try:
            data: datetime = datetime(int(year), int(month), int(day))
            return data
        except ValueError:
            raise ValueError('data must be valid: pt-br format equals dd/mm/aaaa')
