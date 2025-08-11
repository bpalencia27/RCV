from __future__ import annotations
from rcvco.config import settings
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .base import LLMClient

_provider_cache: LLMClient | None = None

def get_llm_client() -> LLMClient:
    global _provider_cache
    if _provider_cache is not None:
        return _provider_cache
    if settings.PROVIDER.lower() == "openai":
        _provider_cache = OpenAIClient(settings.OPENAI_API_KEY, settings.MODEL_NAME)
    else:
        _provider_cache = GeminiClient(settings.GEMINI_API_KEY, settings.GEMINI_MODEL)
    return _provider_cache
