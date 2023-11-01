from datetime import datetime
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    date_joined: datetime


class UpdateUserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    avatar: Optional[InMemoryUploadedFile | str] = None

    class Config:
        arbitrary_types_allowed = True
