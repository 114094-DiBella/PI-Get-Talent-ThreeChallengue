import numpy as np
from models import (
    DocumentOutput,
    EmbeddingsOutput,
    SearchResult,
    SearchOutput,
    QuestionOutput
)
from services.ConnectionCohere import ConnectionCohere

class DocumentService:
    def __init__(self):
        self.conn = ConnectionCohere()
        self.documents = {}
        self.chunks = {}

    def _split_into_chunks(self, text: str, chunk_size: int = 500, overlap: int = 50) -> list:
        """Divide el texto en chunks con overlap"""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            if end > text_len:
                end = text_len
            if end < text_len:
                while end > start and text[end] not in '.!? ':
                    end -= 1
                if end == start:
                    end = start + chunk_size
            
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap if end < text_len else text_len
            
        return chunks
    def _find_relevant_snippet(self, text: str, query_terms: str) -> str:
        """Encuentra el fragmento más relevante del texto basado en los términos de búsqueda"""
        sentences = text.split('.')
        relevant_sentences = []
        # Palabras clave específicas para búsqueda
        query_words = set(query_terms.lower().split()) | {
            'tormenta', 'lluvia', 'miedo', 'viento', 'desorientado',
            'oscuro', 'noche', 'buscar', 'encontrar'
        }
        
        for sentence in sentences:
            sentence = sentence.strip()
            # Verifica si la oración contiene palabras clave
            if any(word in sentence.lower() for word in query_words):
                relevant_sentences.append(sentence)
        
        if not relevant_sentences:
            return text[:200] + "..."
            
        return '. '.join(relevant_sentences[:2]) + '.'


    async def add_document(self, title: str, content: str):
        """Agrega un nuevo documento al sistema"""
        print(f"Valor de entrada: {title}, {content}")
        try:
            doc_id = str(len(self.documents) + 1)
            print(f"Valor de doc_id: {doc_id}")

            chunks = self._split_into_chunks(content)
            print(f"Número de chunks generados: {len(chunks)}")

            self.documents[doc_id] = {
                "title": title,
                "content": content,
                "chunks": chunks
            }

            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}-{i}"
                response = self.conn.cohere.embed(
                    texts=[chunk],
                    model="embed-multilingual-v3.0",
                    input_type="search_document"
                )
                print(f"Generado embedding para chunk {i}")

                self.conn.collection.add(
                    documents=[chunk],
                    metadatas=[{"title": title, "doc_id": doc_id, "chunk_id": chunk_id}],
                    ids=[chunk_id],
                    embeddings=response.embeddings[0]
                )

                self.chunks[chunk_id] = {
                    "content": chunk,
                    "doc_id": doc_id,
                    "embeddings": response.embeddings[0]
                }

            result = DocumentOutput(
                message="Documento subido exitosamente",
                document_id=doc_id
            )
            print(f"Valor de salida: {result.message}, {result.document_id}")
            return result

        except Exception as e:
            print(f"Error en add_document: {str(e)}")
            raise Exception(f"Error al agregar documento: {str(e)}")

    async def add_embeddings(self, documentId: str):
        """Genera embeddings para un documento específico"""
        print(f"Valor de entrada: {documentId}")
        try:
            if documentId not in self.documents:
                raise ValueError(f"Documento con ID {documentId} no encontrado")
                
            doc = self.documents[documentId]
            chunks = doc.get("chunks", [doc["content"]])
            
            for i, chunk in enumerate(chunks):
                response = self.conn.cohere.embed(
                    texts=[chunk],
                    model="embed-multilingual-v3.0",
                    input_type="search_document"
                )
                chunk_id = f"{documentId}-{i}"
                self.chunks[chunk_id] = {
                    "content": chunk,
                    "embeddings": response.embeddings[0]
                }
            
            result = EmbeddingsOutput(
                message="Embeddings generados exitosamente",
                document_id=documentId
            )
            print(f"Valor de salida: {result.message}, {result.document_id}")
            return result
        except Exception as e:
            print(f"Error en add_embeddings: {str(e)}")
            raise Exception(f"Error al generar embeddings: {str(e)}")

    async def search(self, query: str):
        """Busca documentos relevantes basados en la consulta"""
        print(f"Valor de entrada: {query}")
        try:
            print(f"Estado actual de documents: {self.documents}")
            print(f"Estado actual de chunks: {self.chunks}")
            query_embedding = self.conn.cohere.embed(
                texts=[query],
                model="embed-multilingual-v3.0",
                input_type="search_query"
            ).embeddings[0]
            
            results = self.conn.collection.query(
                query_embeddings=[query_embedding],
                n_results=3,
                include=["documents", "distances", "metadatas"]
            )
            print(f"Resultados de ChromaDB: {results}")
            search_results = []
            seen_docs = set()
            
            if results and len(results['ids'][0]) > 0:
                print(f"Encontrados {len(results['ids'][0])} resultados")
                for i in range(len(results['ids'][0])):
                    chunk_id = results['ids'][0][i]
                    doc_id = chunk_id.split('-')[0]
                    distance = results['distances'][0][i]
                    print(f"Procesando chunk_id: {chunk_id}, doc_id: {doc_id}")  # Debug
                    
                    if doc_id not in self.documents:
                        print(f"Advertencia: doc_id {doc_id} no encontrado en documents")
                        continue
                    
                    distance = results['distances'][0][i]
                    chunk_text = results['documents'][0][i]
                    
                    if doc_id not in seen_docs:
                        seen_docs.add(doc_id)
                        doc = self.documents[doc_id]
                        
                        content_snippet = self._find_relevant_snippet(chunk_text, query)
                        
                        search_results.append(SearchResult(
                            document_id=doc_id,
                            title=doc["title"],
                            content_snippet=content_snippet,
                            similarity_score=float(1 - distance)
                        ))

            result = SearchOutput(results=search_results)
            print(f"Valor de salida: {result.results}")
            return result
            
        except Exception as e:
            print(f"Error en search: {str(e)}")
            raise Exception(f"Error en búsqueda: {str(e)}")

    async def ask(self, question: str):
        """Genera una respuesta basada en los documentos relevantes"""
        print(f"Valor de entrada: {question}")
        try:
            search_results = await self.search(question)
            
            context = "\n\n".join([
                f"Documento '{result.title}':\n{result.content_snippet}"
                for result in search_results.results[:3]
            ])
            print(f"Contexto generado: {context[:200]}...")
            
            prompt = f"""Basándote en el siguiente contexto, responde la pregunta de manera clara y concisa.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""
            print(f"Prompt generado: {prompt[:200]}...")
            
            response = self.conn.cohere.generate(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7,
                model='command-r-plus-08-2024'
            )
            
            result = QuestionOutput(
                question=question,
                answer=response.generations[0].text.strip()
            )
            print(f"Valor de salida: {result.question}, {result.answer}")
            return result
            
        except Exception as e:
            print(f"Error en ask: {str(e)}")
            raise Exception(f"Error al responder pregunta: {str(e)}")