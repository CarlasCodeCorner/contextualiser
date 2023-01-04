import json
import logging
from query_services.MongoDBService import MongoDBService
from query_services.ElasticsearchDBService import ElasticsearchDBService
from models.DocumentUploadedDocument import DocumentUploadedDocument
from models.LangDetectedDocument import LangDetectedDocument

logger = logging.getLogger(__name__)


def save_p(payload: dict, channel):
    status = payload['status']

    if status == 'new_document_uploaded':
        
        payload['headers'] = {"X-Tika-PDFextractInlineImages": "true"}

        document_uploaded_document = DocumentUploadedDocument.parse_obj(
                payload)

        # 1.--> save to mongo
        _mongo_id = MongoDBService().save_to_mongo(document_uploaded_document.dict())
        document_uploaded_document.mongo_id = str(_mongo_id)

        
        print(" [x] document saved | mongo_id: %r" %
              document_uploaded_document.mongo_id)

      
        # 3. --> for extraction
        payload = json.dumps(document_uploaded_document.dict(by_alias=True))
        channel.basic_publish(exchange='extraction',
                              routing_key="",
                              body=payload)

    if status == 'lang_detected':
        lang_detect_document = LangDetectedDocument.parse_obj(payload)

       

        print(
            f' [x] det lang {lang_detect_document.lang} & saved to ES | es_id: %r'
            % str(lang_detect_document.es_id))
        print(f' [x] document processed| es_id: %r' %
              lang_detect_document.es_id)


    return payload


def convert_to_dict(paragraphs):
    arr = []
    for i in range(len(paragraphs)):
        dict_test = {}
        for (k, a) in paragraphs[i]:
            dict_test[k] = str(a)
        arr.append(dict_test)
    return arr