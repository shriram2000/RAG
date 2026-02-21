from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.config import settings
from app.rag.embeddings import EmbeddingService
from app.rag.llm import OllamaClient
from app.rag.vector_store import VectorStore

try:
    from langfuse import Langfuse
except Exception:  # pragma: no cover
    Langfuse = None


class AgentState(TypedDict):
    question: str
    contexts: list[dict]
    answer: str


class AgenticRAG:
    def __init__(self) -> None:
        self.embedder = EmbeddingService()
        self.store = VectorStore()
        self.llm = OllamaClient()
        self.graph = self._build_graph()
        self.langfuse = self._build_langfuse_client()

    def _build_langfuse_client(self):
        if not Langfuse or not settings.langfuse_public_key or not settings.langfuse_secret_key:
            return None
        return Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )

    def _retrieve(self, state: AgentState) -> AgentState:
        qvec = self.embedder.embed_query(state["question"])
        contexts = self.store.search(qvec, top_k=settings.top_k)
        return {**state, "contexts": contexts}

    def _generate(self, state: AgentState) -> AgentState:
        context_block = "\n\n".join(
            [f"Source: {c['source']}\nContent: {c['text']}" for c in state["contexts"]]
        )
        prompt = (
            "You are a production assistant. Use only retrieved context. "
            "If missing information, say you do not have enough context.\n\n"
            f"Question: {state['question']}\n\n"
            f"Context:\n{context_block}\n\n"
            "Answer with concise bullet points and include key caveats."
        )
        answer = self.llm.generate(prompt)
        return {**state, "answer": answer}

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("generate", self._generate)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)
        return graph.compile()

    def ask(self, question: str) -> tuple[str, list[str]]:
        trace = self.langfuse.trace(name="rag_ask", input={"question": question}) if self.langfuse else None
        out = self.graph.invoke({"question": question, "contexts": [], "answer": ""})
        sources = sorted({c["source"] for c in out["contexts"]})
        if trace:
            trace.update(output={"answer": out["answer"], "sources": sources})
        return out["answer"], sources
