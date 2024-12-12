from pydantic import BaseModel, Field

class DocumentInput(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)