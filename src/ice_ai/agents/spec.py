from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class AgentSpec:
    """
    Descrizione formale e statica di un agente ICE-AI.

    NON contiene:
    - logica
    - implementazione
    - dipendenze runtime

    Serve per:
    - catalogazione
    - routing
    - introspezione
    - validazione orchestratore
    """

    # ------------------------------------------------------------------
    # IDENTITÀ
    # ------------------------------------------------------------------

    name: str
    description: str

    # ------------------------------------------------------------------
    # DOMINI FUNZIONALI
    # (es: code, logs, workflow, system, knowledge)
    # ------------------------------------------------------------------

    domains: Set[str]

    # ------------------------------------------------------------------
    # RUOLI LOGICI
    # ------------------------------------------------------------------

    is_planner: bool = False
    is_executor: bool = False
    is_observer: bool = False
    is_system: bool = False

    # ------------------------------------------------------------------
    # CAPACITÀ DICHIARATE
    # (string-based per evitare coupling)
    # ------------------------------------------------------------------

    capabilities: Set[str] = field(default_factory=set)

    # ------------------------------------------------------------------
    # METADATA OPZIONALE
    # ------------------------------------------------------------------

    version: Optional[str] = None
    experimental: bool = False
    deprecated: bool = False

    # ------------------------------------------------------------------
    # UI / PRESENTATION HINTS
    # ------------------------------------------------------------------

    ui_label: Optional[str] = None
    ui_group: Optional[str] = None

    # ------------------------------------------------------------------
    # SERIALIZZAZIONE
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "domains": sorted(self.domains),
            "roles": {
                "planner": self.is_planner,
                "executor": self.is_executor,
                "observer": self.is_observer,
                "system": self.is_system,
            },
            "capabilities": sorted(self.capabilities),
            "version": self.version,
            "experimental": self.experimental,
            "deprecated": self.deprecated,
            "ui": {
                "label": self.ui_label,
                "group": self.ui_group,
            },
        }
