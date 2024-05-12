from typing import Optional
from pydantic import BaseModel


class UserBO(BaseModel):
    id: Optional[str] = None
    token_id: Optional[str] = None
    username: str
    email: Optional[str] = None
    password: str