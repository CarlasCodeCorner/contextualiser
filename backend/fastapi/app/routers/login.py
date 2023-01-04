import logging

from fastapi import APIRouter, Depends, HTTPException
from app.services.UserService import UserService
from app.dependencies import auth
from fastapi.security import OAuth2PasswordRequestForm

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/login', tags=['login'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_service = UserService()
    db_user = user_service.get_user_by_username(username=form_data.username)
    if auth.verify_password(form_data.password, db_user.hashed_password):
        token = auth.create_access_token(db_user)
        return {'access_token': token, 'token_type': 'Bearer'}
    raise HTTPException(status_code=401, detail='Password incorrect')