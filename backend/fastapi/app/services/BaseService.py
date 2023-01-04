import logging
import os
from fastapi import Response
from pymongo import MongoClient

logger = logging.getLogger(__name__)

MONGO_USERNAME=os.environ.get('MONGO_USERNAME',"test_user")
MONGO_PASSWORD=os.environ.get('MONGO_PASSWORD',"c0nt5xt!")
MONGO_HOST=os.environ.get('MONGO_HOST',"localhost")
MONGO_PORT=os.environ.get('MONGO_PORT',"27017")
MONGO_COLLECTION=os.environ.get('MONGO_COLLECTION', 'contextualiser')

class BaseService:
    """ initialises the connection the MongoDB and project related variables using ENV Variables
        Input: project_id:str
        Output: self.project_id, self.projects, self.es, self.db
    """
    def __init__(self):
        try:
            self.connection_uri= f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_COLLECTION}'
            self.client = MongoClient(self.connection_uri)
            self.db = self.client.contextualiser
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

   

            
            