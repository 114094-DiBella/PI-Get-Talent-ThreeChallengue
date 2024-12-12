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
from services.ConnectionCohere import ConnectionCohere  

class DocumentService:
    def __init__(self):
        self.conn = ConnectionCohere()  
        self.documents = {}

    async def add_document(self,  title, content):       
        try:
            # Generar Id de documento
            id = len(self.documents) + 1
            # Guardar el documento en la base de datos
            self.documents[id] = {"title": title, "content": content}
            # Generar embeddings
            response = self.conn.cohere.embed(
                texts=[content],
                model="embed-multilingual-v3.0"
            )
            # Guardar embeddings en la base de datos
            self.documents[id]["embeddings"] = response.embeddings[0]
            # Retornar documento
            document = DocumentOutput(
            message="Documento subido exitosamente",
            document_id=id
            )
            return document
        except Exception as e:
            raise Exception(f"Error al agregar documento: {str(e)}")
        
    async def add_embeddings(self, documentId, embeddings):
        try:
            # Guardar embeddings en la base de datos
            self.documents[documentId]["embeddings"] = embeddings
            embedding = EmbeddingsOutput(
                document_id=documentId

            )
            return embedding
        except Exception as e:
            raise Exception(f"Error al agregar embeddings: {str(e)}")
        

    async def search(self, query):
        try:
            # Generar embedding para la consulta
            query_embedding = self.conn.cohere.embed(
                texts=[query],
                model="embed-multilingual-v3.0"
            ).embeddings[0]
            
            search_results = []

            for doc_id, doc in self.documents.items():
                if "embeddings" in doc:
                    similarity = self._calculate_similarity(query_embedding, doc["embeddings"])
                    search_results.append(SearchResult(
                        document_id=doc_id,
                        title=doc["title"],
                        content_snippet=doc["content"][:200] + "...",
                        similarity_score=similarity
                    ))

            return SearchOutput(results=search_results[:5])
            
        except Exception as e:
            raise Exception(f"Error en búsqueda: {str(e)}")

    async def ask(self, question):   
        try:
            relevant_docs = await self.search(question)
            
            context = "\n\n".join([doc.content_snippet for doc in relevant_docs.results[:3]])
            
            response = self.conn.cohere.generate(
                prompt=f"Contexto: {context}\n\nPregunta: {question}\n\nRespuesta:",
                max_tokens=300,
                temperature=0.7,
                model='command'
            )
            
            return QuestionOutput(
                question=question,
                answer=response.generations[0].text.strip()
            )
            
        except Exception as e:
            raise Exception(f"Error al responder pregunta: {str(e)}")


