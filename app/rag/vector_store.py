from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.config import settings


class VectorStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection = settings.collection_name

    def ensure_collection(self, dim: int) -> None:
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection not in collections:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, vectors: list[list[float]], texts: list[str], source: str) -> int:
        self.ensure_collection(len(vectors[0]))
        points = [
            PointStruct(id=idx, vector=vec, payload={"text": txt, "source": source})
            for idx, (vec, txt) in enumerate(zip(vectors, texts, strict=True))
        ]
        self.client.upsert(collection_name=self.collection, points=points)
        return len(points)

    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
        )
        return [
            {
                "text": r.payload.get("text", ""),
                "source": r.payload.get("source", "unknown"),
                "score": r.score,
            }
            for r in results
        ]
