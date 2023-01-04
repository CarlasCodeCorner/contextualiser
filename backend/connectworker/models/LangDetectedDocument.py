from models.DocumentPayload import DocumentPayload
from models.TextExtractedDocument import TextExtractedDocument

class LangDetectedDocument(TextExtractedDocument):
    lang: str