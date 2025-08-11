from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol

class LLMClient(ABC):
    @abstractmethod
    def generate_report(self, prompt: str) -> str:  # pragma: no cover
        ...

class SupportsGenerate(Protocol):
    def generate_report(self, prompt: str) -> str: ...
