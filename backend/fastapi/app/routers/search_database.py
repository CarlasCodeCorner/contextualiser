
import logging
from fastapi import APIRouter, status, Depends
from app.models.Search import Search
from app.dependencies import auth
from app.services.SearchService import SearchService

logger = logging.getLogger(__name__)

router = APIRouter()    

@router.get('/search/{project_id}/keyword/{keyword}', tags=['search_database'], dependencies=[Depends(auth.check_role)])

async def search_mongodb(project_id:str, keyword:str):
  
    search_service= SearchService(project_id=project_id)
    response = search_service.search_keyword(keyword=keyword)
    return response