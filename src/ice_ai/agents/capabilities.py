from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, Dict, Any


@dataclass(frozen=True)
class AgentCapabilities:
    """
    Mappa dichiarativa delle capacità di un agente.

    NON contiene logica.
    NON dipende dall'engine.
    Serve per:
    - routing
    - planning
    - introspezione
    - policy
    - UI / CLI
    """

    # Ruoli logici
    is_planner: bool = False
    is_executor: bool = False
    is_observer: bool = False
    is_system: bool = False

    # Dipendenze funzionali
    uses_llm: bool = False
    uses_internal_codemodel: bool = False
    uses_knowledge: bool = False

    # Flags di governance
    experimental: bool = False
    deprecated: bool = False

    # Capacità semantiche (libere, non enum)
    capabilities: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "roles": {
                "planner": self.is_planner,
                "executor": self.is_executor,
                "observer": self.is_observer,
                "system": self.is_system,
            },
            "dependencies": {
                "llm": self.uses_llm,
                "internal_codemodel": self.uses_internal_codemodel,
                "knowledge": self.uses_knowledge,
            },
            "flags": {
                "experimental": self.experimental,
                "deprecated": self.deprecated,
            },
            "capabilities": sorted(self.capabilities),
        }

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    def with_capability(self, *caps: str) -> "AgentCapabilities":
        """
        Ritorna una nuova istanza con capability aggiunte.
        (immutabilità preservata)
        """
        return AgentCapabilities(
            is_planner=self.is_planner,
            is_executor=self.is_executor,
            is_observer=self.is_observer,
            is_system=self.is_system,
            uses_llm=self.uses_llm,
            uses_internal_codemodel=self.uses_internal_codemodel,
            uses_knowledge=self.uses_knowledge,
            experimental=self.experimental,
            deprecated=self.deprecated,
            capabilities=self.capabilities.union(caps),
        )
