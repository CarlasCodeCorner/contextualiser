from pydantic import BaseModel
from typing import Optional,List

class Upload(BaseModel):
    text: str
    tag: Optional[List[str]]