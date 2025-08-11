from __future__ import annotations
from .base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def generate_report(self, prompt: str) -> str:  # pragma: no cover (simulación)
        return f"[openai:{self.model}] {prompt[:200]}"
