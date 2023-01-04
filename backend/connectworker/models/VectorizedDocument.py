from typing import List

from pydantic import BaseModel
from models.TextExtractedDocument import TextExtractedDocument


class VectorizedDocument(TextExtractedDocument):
    vector: List[List[float]]

