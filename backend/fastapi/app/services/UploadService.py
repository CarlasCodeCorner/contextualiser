import json
import logging
import pika
from fastapi import Response

from app.pika_connector import setup_pika
from app.services.BaseService import BaseService

logger = logging.getLogger(__name__)
TOPIC_CONNECT = 'connect'
class UploadService(BaseService):
                
    def new_upload(self, files):
        try:
           
            pika_channel, _ = setup_pika(TOPIC_CONNECT)
            documents = []
            
            document = files.dict()
            document['upload_source']="direct_upload"
            document['length_str']=len(files.text)
            
            logger.info("/database upload of new text: " + str(files.text))
                
            properties = pika.BasicProperties(content_type="application/json") 


            document['status'] = 'new_document_uploaded'
                
            payload = json.dumps(document)
                
            pika_channel.basic_publish(exchange=TOPIC_CONNECT, routing_key='', body=payload, properties=properties)

            return Response(content=f'Uploaded {len(documents)} new texts', status_code=200, media_type='application/json')
        
        except Exception as e:
            logger.error(f'Could not upload new text. {e}')
            return Response(content='Could not upload new text. {e}', status_code=404)