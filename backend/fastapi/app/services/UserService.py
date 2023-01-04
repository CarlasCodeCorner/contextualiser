import json
import logging
import os

from app.dependencies import auth
from app.models.User import User
from bson import ObjectId
from fastapi import HTTPException, Response
from pymongo import MongoClient


logger = logging.getLogger(__name__)

MONGO_USERNAME = os.environ.get('MONGO_USERNAME', "test_user")
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', "c0nt5xt!")
MONGO_HOST = os.environ.get('MONGO_HOST', "localhost")
MONGO_PORT = os.environ.get('MONGO_PORT', "23456")
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'contextualiser')


class UserService():

    def __init__(self):
        try:
            self.connection_uri = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_COLLECTION}'
            self.client = MongoClient(self.connection_uri)
            self.db = self.client.contextualiser
            self.users = self.db.users
            self.roles = self.db.roles

        except Exception:
            logger.error(f"Database connection failed")

  

    #######################
    ##- CREATE NEW USER ###
    #######################

    def create_user(self, user: User, project_id: str) -> Response:
        """creates new user. The user_id is automatically generated.

        Args:
            user (User):
                class User(BaseModel):
                    email: EmailStr
                    username: str
                    password: str

        Returns:
            Response: _description_
        """
        try:
            user_dict = user.dict(by_alias=True)
            _id = str(ObjectId())
            user_dict["_id"] = _id
            hashed_password = auth.create_password_hash(user.password)
            user_dict['hashed_password'] = hashed_password
            self.users.insert_one(user_dict)
            return Response(content=f'Successfully created user: {_id}',
                            status_code=201)
        except:
            raise HTTPException(detail=f'Could not create user',
                                status_code=400)

    ####################
    ##- UPDATE USERS ###
    ####################

    def update_user(self, user: User) -> Response:
        """update one user information

        Args:
            user (user): user model class

        Returns:
            Response: Status Code
        """
        try:
            user_id = user.id

            user_update_dict = {
                'email': user.email,
                'username': user.username,
                'password': user.password
            }
    

            self.users.update_one({'_id': user_id}, {'$set': user_update_dict},
                                  upsert=False)
        except Exception:
            logger.error(f'Could not update user {user_id} in MongoDB')
            return Response(content=f'Could not update user in MongoDB',
                            status_code=400)

    ###########################
    ##- ADD PROJECT TO USER ###
    ###########################

    def update_user_add_project(self, user_id: str, project_id: str,
                                role: str) -> Response:
        """Add project to user. Will be overidden if already exists.

        Args:
            user_id (str): unique identifier
            project_id (str): unique identifier

        Returns:
            Response: OK, 200
        """
        try:
            user = self.get_user_by_id(user_id)
            user = json.loads(user.body)
           
             
            user['role'].append({'project_id': project_id, 'role': role})
            user["_id"] = user_id
            del user['id']
            self.users.update_one({'_id': user_id}, {'$set': user},
                                upsert=False)
            return Response(content='User was sucessfully updated',
                    status_code=200)

        except Exception:
            logger.error(f'Could not update user {user_id} in MongoDB.')
            return Response(content=f'Could not update document in MongoDB.')


    ###################
    ##- DELETE USER ###
    ###################


    def delete_user_from_all_projects(self, user_id: str) -> Response:
        try:
            user_document = self.users.find_one({'_id': user_id})
            user = User.parse_obj(user_document)
            user_dict = user.dict(by_alias=True)
            self.users.delete_one({'_id': user_dict['_id']})
            return Response(status_code=200)
        except Exception:
            logger.error(f'Could not delete user {user_id} in project.')
            return Response(
                content=f'Could not delete user {user_id} in project.',
                status_code=400)


    ##################################
    ##- GET USERS FROM ALL PROJECTS ##
    ##################################

    def get_users(self) -> Response:
        """Returns list of users from all projects

        Returns:
            Response: List of users from all projects
        """
        try:
            response = list(self.users.find())
            return Response(content=json.dumps(response),
                            status_code=200,
                            media_type='application/json')
        except Exception as e:
            logger.error(f'Getting users failed. {e}')
            return Response(content=f'Could not find users. {e}')

    ####################
    ##- GET ONE USER ###
    ####################

    def get_user_by_id(self, user_id: str) -> Response:
        """gets one user by id

        Args:
            user_id (str): unique identifier for project

        Returns:
            Response: user:dict
        """
        try:
            users_document = self.users.find_one({'_id': user_id})
            user = User.parse_obj(users_document)
            return Response(content=json.dumps(user.dict()),
                            status_code=200,
                            media_type='application/json')
        except Exception as e:
            logger.error(f'Getting user failed. {e}')
            return Response(
                content=f'Could not retrieve user with user_id: {user_id}. {e}',
                status_code=400)

    ################################
    ##- GET ONE USER BY USERNAME ###
    ################################

    def get_user_by_username(self, username: str):
        """gets one user by username

        Args:
            username (str): unique identifier for project

        Returns:
            Response: user:dict
        """
        try:
            users_document = self.users.find_one({'username': username})
            user = User.parse_obj(users_document)
            return user
        except Exception as e:
            logger.error(f'Getting user failed. {e}')
            return Response(
                content=f'Could not retrieve user with user_id: {username}. {e}',
                status_code=400)

    ##################################
    ##- GET ALL ROLES FROM PROJECT ###
    ##################################
    def get_roles(self) -> Response:
        """Returns list of roles from one project

        Returns:
            Response: List of roles from one project
        """
        try:
            result = []
            response = list(self.roles.find())
            for resp in response:
                result.append(resp['role'])
            return Response(content=json.dumps(result),
                            status_code=200,
                            media_type='application/json')
        except Exception as e:
            logger.error(f'Getting roles failed. {e}')
            return Response(content=f'Could not find roles. {e}')
