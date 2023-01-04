from typing import List

from pydantic import BaseModel
from models.DocumentPayload import DocumentPayload

class Paragraph(BaseModel):
    paragraph_id: str
    text: str

class TextExtractedDocument(DocumentPayload):
    paragraphs: List[Paragraph]

