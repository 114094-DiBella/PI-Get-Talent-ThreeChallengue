from pydantic import BaseModel


class EmbeddingsInput(BaseModel):
    message: str
    document_id: str