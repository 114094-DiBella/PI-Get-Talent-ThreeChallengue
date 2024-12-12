from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    document_id: int
    title: str = Field(..., min_length=1)
    content_snippet: str = Field(..., min_length=1)