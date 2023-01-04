from typing import List
from pydantic import BaseModel, Field
from models.DocumentPayload import DocumentPayload

class HeaderDocument(BaseModel):
    pdf_extract_inline_images: str = Field(default='', alias='X-Tika-PDFextractInlineImages')
   

class DocumentUploadedDocument(DocumentPayload):
    text: str = ''
    tag:List[str]
    length_str: int
    upload_source: str
    


    
