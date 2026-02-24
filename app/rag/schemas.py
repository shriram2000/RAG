from pydantic import BaseModel, HttpUrl


class IngestResponse(BaseModel):
    chunks_indexed: int
    source: str
    images_detected: int = 0


class URLIngestRequest(BaseModel):
    url: HttpUrl


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
