import logging
from fastapi import Response
import json
from app.services.BaseService import BaseService

logger = logging.getLogger(__name__)

class SearchService(BaseService):
    
    def search_keyword(self, keyword:str):
        """searches the elasticsearch index of a project 

        Args:
            project_id (str): id of current project
            keyword (str)): text

        Returns:
            _type_: _description_
        """
        try:
            index = self.project_id +'_index'
            resp = self.es.search(index=index, query = {"match": {"doc_text":keyword}}, size = '10000')
        
            data = [i['_source'] for i in resp['hits']['hits']]
            return Response(content=json.dumps(data), status_code=200, media_type='application/json')
        
        except Exception as e:
            logger.error(f'Could not find any entries for keyword {keyword}')
            return Response(content=f'Could not find any entries for {keyword}', status_code=400)
        
    