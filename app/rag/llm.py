import httpx

from app.config import settings


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = settings.ollama_url.rstrip("/")
        self.model = settings.ollama_model

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        response = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=90)
        response.raise_for_status()
        return response.json().get("response", "")
