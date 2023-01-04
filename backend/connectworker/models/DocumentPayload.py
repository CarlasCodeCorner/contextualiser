
from typing import List, Optional
from pydantic import BaseModel

class DocumentPayload(BaseModel):
    
    mongo_id: Optional[str]
    status:str = ''
