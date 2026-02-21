from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from prometheus_client import Counter, generate_latest

from app.rag.agent import AgenticRAG
from app.rag.chunking import chunk_text
from app.rag.downloader import download_url_to_folder
from app.rag.embeddings import EmbeddingService
from app.rag.parsing import DocumentParser
from app.rag.schemas import ChatRequest, ChatResponse, IngestResponse, URLIngestRequest
from app.rag.vector_store import VectorStore

app = FastAPI(title="Open-Source Agentic RAG", version="0.2.0")
ingest_counter = Counter("rag_ingest_requests_total", "Number of ingest requests")
chat_counter = Counter("rag_chat_requests_total", "Number of chat requests")

agent = AgenticRAG()
embedder = EmbeddingService()
store = VectorStore()
parser = DocumentParser()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> bytes:
    return generate_latest()


def _index_file(path: Path, source_label: str) -> IngestResponse:
    text, images = parser.parse_with_artifacts(str(path))
    chunks = chunk_text(text)
    vectors = embedder.embed_texts(chunks)
    count = store.upsert(vectors=vectors, texts=chunks, source=source_label)
    return IngestResponse(chunks_indexed=count, source=source_label, images_detected=len(images))


@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)) -> IngestResponse:
    ingest_counter.inc()
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / (file.filename or "uploaded_document")
    destination.write_bytes(await file.read())
    return _index_file(destination, destination.name)


@app.post("/ingest/url", response_model=IngestResponse)
def ingest_url(payload: URLIngestRequest) -> IngestResponse:
    ingest_counter.inc()
    downloaded = download_url_to_folder(str(payload.url))
    return _index_file(downloaded, downloaded.name)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    chat_counter.inc()
    answer, sources = agent.ask(request.question)
    return ChatResponse(answer=answer, sources=sources)
