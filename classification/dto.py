from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from pydantic import BaseModel


class CreateImageDTO(BaseModel):
    user_id: int
    title: str
    image: Optional[UploadedFile | str] = None

    class Config:
        arbitrary_types_allowed = True


class ImageDTO(BaseModel):
    id: int
    user_id: int
    title: str
    image: str
