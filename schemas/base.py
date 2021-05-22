from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = 'forbid'
