from pydantic import BaseModel


class EmbeddingsOutput(BaseModel):
    document_id: int