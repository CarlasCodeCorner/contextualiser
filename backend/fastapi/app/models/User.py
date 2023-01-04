from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class Project_Role(BaseModel):
    role: str

class User(BaseModel):
    id: Optional[str] = Field(default='', alias='_id')
    email: EmailStr
    username: str
    password: str
    role: List[Project_Role]
    hashed_password: Optional[str]


    class Config:
        use_enum_values = True