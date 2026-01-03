from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Protocol, List


# ---------------------------------------------------------------------
# TIPI CANONICI (COGNITIVE LAYER)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class LLMMessage:
    """
    Messaggio canonico per interazione LLM.
    NON contiene semantica runtime.
    """
    role: str
    content: str


@dataclass(frozen=True)
class LLMCompletion:
    """
    Risultato canonico di una chiamata LLM.
    """
    text: str
    raw: Any
    usage: Dict[str, Any]


# ---------------------------------------------------------------------
# INTERFACCIA ASTRATTA LLM
# ---------------------------------------------------------------------

class LLMAdapter(Protocol):
    """
    Interfaccia astratta per un adapter LLM.

    ⚠️ NON implementa backend
    ⚠️ NON conosce OpenAI / Ollama / HTTP
    ⚠️ NON legge env
    ⚠️ NON fa retry

    Serve solo per:
    - typing
    - reasoning
    - dependency inversion
    """

    def complete(
        self,
        messages: List[LLMMessage],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        json_mode: bool = False,
        extra: Dict[str, Any] | None = None,
    ) -> LLMCompletion:
        ...

    def chat(
        self,
        messages: Iterable[LLMMessage],
        **kwargs: Any,
    ) -> LLMCompletion:
        ...
