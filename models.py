from pydantic import BaseModel, Field
from typing import List

class DocumentInput(BaseModel):
    title: str = Field(..., description="Título del documento")
    content: str = Field(..., description="Contenido del documento")

class DocumentOutput(BaseModel):
    message: str
    document_id: str

class EmbeddingsInput(BaseModel):
    document_id: str

class EmbeddingsOutput(BaseModel):
    message: str
    document_id: str

class SearchResult(BaseModel):
    document_id: str
    title: str
    content_snippet: str
    similarity_score: float

class SearchInput(BaseModel):
    query: str

class SearchOutput(BaseModel):
    results: List[SearchResult]

class QuestionInput(BaseModel):
    question: str

class QuestionOutput(BaseModel):
    question: str
    answer: str