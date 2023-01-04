import logging
import os
from elasticsearch import Elasticsearch
from models.DocumentUploadedDocument import DocumentUploadedDocument
import datetime
import json
import pytz

logger = logging.getLogger(__name__)

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', 'http://localhost:9200')

# TODO: classes should be lowercase
class ElasticsearchDBService():

    def __init__(self):
        try:
            self.es = Elasticsearch(ELASTICSEARCH_URL)
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

    def save_to_es(self, doc: DocumentUploadedDocument) -> DocumentUploadedDocument:
        """Saves Documents as index to Elasticsearch Database

        Args:
            doc (DocumentUploadedDocument): Documents details contains mongo id, upload_source,
            doc_text, created_at, filename, filetype, vector, tags, lang

        Returns:
            DocumentUploadedDocument: uploaded Documents details
        """

        try:
            if doc.groups[0]==' ':
                groups = None
            else:
                groups = doc.groups
            
            #get current local time 
            timeInBerlin = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
            currentTimeInBerlin = timeInBerlin.strftime("%D %H:%M:%S")
            
            new_document= {
                'mongo_id': doc.mongo_id,
                'upload_source':doc.upload_source,
                'doc_text': None,
                'created_at': str(currentTimeInBerlin),
                'filename': doc.file_name,
                'filetype': doc.filetype,
                'vector':None,
                'groups': groups,
                'lang':None,
            }
            
            try:
                for filt in doc.filters:
                    try: 
                        new_document[filt]
                    except:
                        new_document[filt] = ''
            except:
                pass
            
            es_index_id = doc.es_index_id
            res = self.es.index(index=es_index_id, document= json.dumps(new_document))
            es_id = res.body['_id']
            # body -> {'_index': 'docubot', '_id': 'Jr-Y9YABYF3ut8q3AyNx', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 2, '_primary_term': 2}
            return es_id
        except Exception as e:
            logger.error(f"Couldn't save this Document id {es_index_id} in Elasticsearch Databse")

    # TODO: Difference between es_id & es_index_id ?
    # TODO: Shouldnt have a return value
    def update_es_by_id(self, es_id: str, parameter_name: str, parameter_value, es_index_id: str) -> str:
        """Updates es index by ID.

        Args:
            es_id (str): Elasticsearch index ID
            parameter_name (str): _description_
            parameter_value (_type_): _description_ ?
            es_index_id (str): Elasticsearch index ID ?

        Raises:
            Response: Errormessage containing es ID

        Returns:
            str: Message about sucessful update 
        """
        try:
            if parameter_name == "doc_text":
                self.es.update(index=es_index_id, id=es_id,
                                doc = {parameter_name: json.dumps(parameter_value)})
            else:
                self.es.update(index=es_index_id, id= es_id,
                                doc= {parameter_name: parameter_value})
            return f'doc: {es_id} field {parameter_name} updated successfully.'
        except Exception as e:
            logger.error(f'doc: {es_id} field {parameter_name} could not be updated. {e}')
        
        
    def get_es_by_id(self, es_id: str, es_index_id: str) -> dict:
        """Get Document out of Elasticsearch Database.

        Args:
            es_id (str): Elasticsearch index ID
            es_index_id (str): Elasticsearch index ID

        Raises:
            Response: Errormessage containing es ID

        Returns:
            dict: Document dict out of es 
        """
        try:
            res = self.es.get(index=es_index_id, id=es_id)
        
            return res
        except Exception as e:
            logger.error(f'Could not get Document {es_id}')
    
