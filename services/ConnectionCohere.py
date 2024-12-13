import os
from chromadb import Client, Settings
import cohere
from dotenv import load_dotenv

class ConnectionCohere:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        
        # Obtener API key
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("No se encontró COHERE_API_KEY en las variables de entorno")
        
        # Inicializar Cohere
        self.cohere = cohere.Client(self.api_key)
        
        # Inicializar ChromaDB
        self.chroma = Client(Settings(is_persistent=True))
        
        # Obtener o crear colección
        try:
            # Intentar obtener la colección existente
            self.collection = self.chroma.get_collection(name="documents")
        except:
            # Si no existe, crearla
            self.collection = self.chroma.create_collection(name="documents")

    def reset_collection(self):
        """Reinicia la colección de documentos"""
        try:
            if "documents" in self.chroma.list_collections():
                self.chroma.delete_collection("documents")
            self.collection = self.chroma.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            print("Colección reiniciada exitosamente")
        except Exception as e:
            print(f"Error al reiniciar colección: {str(e)}")
            raise

