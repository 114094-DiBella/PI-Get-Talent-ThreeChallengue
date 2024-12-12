from pydantic import BaseModel, Field

from models.SearchResult import SearchResult

class SearchOutput(BaseModel):
    resultados: list[SearchResult] 