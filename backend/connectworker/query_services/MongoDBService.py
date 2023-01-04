import os
import logging
from bson import ObjectId
from pydantic import Json
from pymongo import MongoClient
from models.DocumentUploadedDocument import DocumentUploadedDocument

logger = logging.getLogger(__name__)

# Connection details for container user
MONGO_USERNAME=os.environ.get('MONGO_USERNAME',"test_user")
MONGO_PASSWORD=os.environ.get('MONGO_PASSWORD',"c0nt5xt!")
MONGO_HOST=os.environ.get('MONGO_HOST',"localhost")
MONGO_PORT=os.environ.get('MONGO_PORT',"23456")
MONGO_COLLECTION=os.environ.get('MONGO_COLLECTION', 'contextualiser')

# TODO: classes lowercase
class MongoDBService():
    def __init__(self):
        try:
            self.connection_uri= f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authMechanism=DEFAULT&authSource={MONGO_COLLECTION}'
            self.client = MongoClient(self.connection_uri)
            self.db = self.client.contextualiser
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")



    def save_to_mongo(self, uploaded_document: DocumentUploadedDocument) -> DocumentUploadedDocument:
        """Saves document in MongoDB

        Args:
            file (str): Document text
            file_name (str): Name of file
            collection_id (str): Collection id in esDB/mongoDB?

        Raises:
            Response: Errormessage containing MongoDB ID

        Returns:
            ObjectId: Saved Document as an ObjectId object
        """
       
        
        try:
            
            return self.db.texts.insert_one(uploaded_document).inserted_id
        except Exception as e:
                logger.error(f"Couldn't save this Document in MongoDB")

    #### RETRIEVE FROM MONGO ####
    def retrieve_file_by_id(self, _id: str) -> Json:
        """Retrieves document from Gridfs

        Args:
            _id (str): Document ID in Gridfs

        Raises:
            Response: Errormessage containing Gridfs ID

        Returns:
            Json: Document including metadata?
        """
        try:
            _id = ObjectId(_id)
            documents = self.db.documents
            query = {"_id": _id}
            doc = documents.find_one(query)
            
            return doc #json of metadata + file
        except Exception as e:
            logger.error(f"Couldn't retrieve this Document from MongoDB")




