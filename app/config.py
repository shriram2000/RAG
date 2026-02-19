from pydantic import BaseModel
import os


class Settings(BaseModel):
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    collection_name: str = os.getenv("COLLECTION_NAME", "documents")
    top_k: int = int(os.getenv("TOP_K", "6"))


settings = Settings()
