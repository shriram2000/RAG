import json
import os
from typing import Any

import faiss
import numpy as np

from app.config import settings


class VectorStore:
    def __init__(self) -> None:
        self.index_path = settings.index_path
        self.metadata_path = settings.metadata_path
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        self._index: faiss.IndexFlatIP | None = None
        self._metadata: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.index_path):
            self._index = faiss.read_index(self.index_path)
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)

    def _persist(self) -> None:
        if self._index is not None:
            faiss.write_index(self._index, self.index_path)
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, ensure_ascii=False, indent=2)

    def upsert(self, vectors: list[list[float]], texts: list[str], source: str) -> int:
        if not vectors:
            return 0

        arr = np.array(vectors, dtype="float32")
        if self._index is None:
            self._index = faiss.IndexFlatIP(arr.shape[1])

        self._index.add(arr)
        self._metadata.extend({"text": txt, "source": source} for txt in texts)
        self._persist()
        return len(texts)

    def search(self, query_vector: list[float], top_k: int) -> list[dict[str, Any]]:
        if self._index is None or self._index.ntotal == 0:
            return []

        q = np.array([query_vector], dtype="float32")
        scores, indices = self._index.search(q, top_k)

        results: list[dict[str, Any]] = []
        for score, idx in zip(scores[0], indices[0], strict=True):
            if idx < 0 or idx >= len(self._metadata):
                continue
            payload = self._metadata[idx]
            results.append(
                {
                    "text": payload.get("text", ""),
                    "source": payload.get("source", "unknown"),
                    "score": float(score),
                }
            )
        return results
