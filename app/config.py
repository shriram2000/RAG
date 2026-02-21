import os
from pydantic import BaseModel


class Settings(BaseModel):
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    top_k: int = int(os.getenv("TOP_K", "6"))

    index_path: str = os.getenv("FAISS_INDEX_PATH", "data/index/faiss.index")
    metadata_path: str = os.getenv("FAISS_METADATA_PATH", "data/index/metadata.json")
    downloads_dir: str = os.getenv("DOWNLOADS_DIR", "data/downloads")

    langfuse_secret_key: str | None = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_public_key: str | None = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_host: str = os.getenv("LANGFUSE_HOST", "http://localhost:3001")


settings = Settings()
