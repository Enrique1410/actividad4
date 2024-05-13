from typing import Optional
from pydantic import BaseModel


class FileBO(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    content: Optional[str] = None
    user_id:Optional[int] = None
