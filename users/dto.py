from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    date_joined: datetime
