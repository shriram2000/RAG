from pydantic import BaseModel


class IngestResponse(BaseModel):
    chunks_indexed: int


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
