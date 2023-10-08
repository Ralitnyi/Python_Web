from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    email: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthday: Optional[datetime]
    description: str = None


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
