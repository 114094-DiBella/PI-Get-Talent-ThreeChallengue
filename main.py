from fastapi import FastAPI, HTTPException
from typing import List, Dict

from services.DocumentService import DocumentService
from models import (
    DocumentInput, 
    DocumentOutput, 
    EmbeddingsInput, 
    EmbeddingsOutput,
    SearchInput,
    SearchOutput,
    QuestionInput,
    QuestionOutput
)

app = FastAPI(title="RAG System API")
service = DocumentService()

@app.post("/upload", response_model=DocumentOutput)
async def upload_document(document: DocumentInput):
    try:
        result = await service.add_document(
            title=document.title,
            content=document.content
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-embeddings", response_model=EmbeddingsOutput)
async def generate_embeddings(input: EmbeddingsInput):
    try:
        result = await service.add_embeddings(document_id=input.document_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchOutput)
async def search_documents(input: SearchInput):
    try:
        results = await service.search(query=input.query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QuestionOutput)
async def ask_question(input: QuestionInput):
    try:
        answer = await service.ask(question=input.question)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


