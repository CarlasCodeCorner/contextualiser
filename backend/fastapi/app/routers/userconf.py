import logging

from app.dependencies import auth
from app.models.User import User
from app.services.UserService import UserService
from fastapi import APIRouter, Depends


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/user/create/{project_id}',
             tags=['userconf'],
             dependencies=[Depends(auth.check_admin)])
async def create_user(user: User, project_id: str):
    user_service = UserService()
    user_service.create_user(user=user, project_id=project_id)
    pass


@router.delete('/user/delete_from_project/{project_id}/{user_id}',
               tags=['userconf'],
               dependencies=[Depends(auth.check_admin)])
async def delete_user_from_project(project_id: str, user_id: str):
    user_service = UserService()
    response = user_service.delete_user_from_project(project_id=project_id,
                                                     user_id=user_id)
    return response


@router.delete('/user/delete/{user_id}',
               tags=['userconf'],
               dependencies=[Depends(auth.check_admin)])
async def delete_user_from_all_projects(user_id: str):
    user_service = UserService()
    response = user_service.delete_user_from_all_projects(user_id=user_id)
    return response


@router.put('/user/p/{project_id}/u/{user_id}/role/{role}',
            tags=['userconf'],
            dependencies=[Depends(auth.check_admin)])
async def update_user_add_project(project_id: str, user_id: str, role: str):
    user_service = UserService()
    response = user_service.update_user_add_project(project_id=project_id,
                                                    user_id=user_id,
                                                    role=role)
    return response


@router.get('/user/u/{user_id}',
            tags=['userconf'],
            dependencies=[Depends(auth.check_admin)])
async def get_user_by_id(user_id: str):
    user_service = UserService()
    response = user_service.get_user_by_id(user_id=user_id)
    return response


@router.get('/users/get_users_from_project{project_id}',
            tags=['userconf'],
            dependencies=[Depends(auth.check_admin)])
async def get_users_from_project(project_id):
    user_service = UserService()
    response = user_service.get_users_from_project(project_id=project_id)
    return response


@router.get('/users/', tags=['userconf'], dependencies=[Depends(auth.check_admin)])
async def get_users_from_all_p():
    user_service = UserService()
    response = user_service.get_users_from_all_projects()
    return response


@router.get('/existing_roles/', tags=['existing_roles'], dependencies=[Depends(auth.check_admin)])
async def get_roles_as_array():
    user_service = UserService()
    response = user_service.get_roles()
    return response
