from pydantic import BaseModel

class DocumentOutput(BaseModel):
    message: str
    document_id: int