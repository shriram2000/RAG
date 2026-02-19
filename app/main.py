import io

from fastapi import FastAPI, File, UploadFile
from prometheus_client import Counter, generate_latest
from pypdf import PdfReader

from app.rag.agent import AgenticRAG
from app.rag.chunking import chunk_text
from app.rag.embeddings import EmbeddingService
from app.rag.schemas import ChatRequest, ChatResponse, IngestResponse
from app.rag.vector_store import VectorStore

app = FastAPI(title="Open-Source Agentic RAG", version="0.1.0")
ingest_counter = Counter("rag_ingest_requests_total", "Number of ingest requests")
chat_counter = Counter("rag_chat_requests_total", "Number of chat requests")

agent = AgenticRAG()
embedder = EmbeddingService()
store = VectorStore()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> bytes:
    return generate_latest()


@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)) -> IngestResponse:
    ingest_counter.inc()
    content = await file.read()
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages)
    chunks = chunk_text(text)
    vectors = embedder.embed_texts(chunks)
    count = store.upsert(vectors=vectors, texts=chunks, source=file.filename)
    return IngestResponse(chunks_indexed=count)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    chat_counter.inc()
    answer, sources = agent.ask(request.question)
    return ChatResponse(answer=answer, sources=sources)
