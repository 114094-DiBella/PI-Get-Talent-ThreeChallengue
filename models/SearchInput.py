from pydantic import BaseModel, Field
class SearchInput(BaseModel):
    query: str = Field(..., min_length=1)