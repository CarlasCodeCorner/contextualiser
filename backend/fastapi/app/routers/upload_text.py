import logging
from app.models.Upload import Upload
from fastapi import APIRouter, File, UploadFile, Depends
from app.dependencies import auth
from app.services.UploadService import UploadService


logger = logging.getLogger(__name__)

router = APIRouter()    

@router.post('/upload_text/', tags=['upload_text'],dependencies=[Depends(auth.check_role)])
async def upload_text(files: Upload):
    
    uploadService = UploadService()
    response =uploadService.new_upload(files=files)
    return response
