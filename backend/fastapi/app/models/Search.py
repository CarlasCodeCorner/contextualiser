from pydantic import BaseModel, validator, Field

class Search(BaseModel):
    id: str = Field(default='', alias='_id')
    project_name: str = ''