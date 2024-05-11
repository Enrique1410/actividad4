from typing import Optional
from pydantic import BaseModel


class FileBO(BaseModel):
    id: Optional[int] = None
    token_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    content: Optional[str] = None
