from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set


@dataclass(frozen=True)
class AgentSpec:
    """
    AgentSpec — descrizione cognitiva e statica di un agente ICE-AI.

    È la *carta d’identità* dell’agente.

    NON contiene:
    - logica
    - implementazione
    - stato runtime
    - dipendenze engine

    Serve per:
    - catalogazione
    - routing cognitivo
    - planning
    - introspezione
    - validazione orchestratore
    - UI / CLI
    """

    # ==================================================================
    # IDENTITÀ
    # ==================================================================

    name: str
    """
    Nome canonico e univoco dell’agente.
    Usato come chiave primaria nel catalogo.
    """

    description: str
    """
    Descrizione semantica dell’agente (umana + LLM-friendly).
    """

    # ==================================================================
    # DOMINI FUNZIONALI
    # ==================================================================

    domains: Set[str]
    """
    Domini logici in cui l’agente opera.
    Esempi: {"code"}, {"knowledge"}, {"workflow"}, {"system"}
    """

    # ==================================================================
    # RUOLI COGNITIVI
    # ==================================================================

    is_planner: bool = False
    is_executor: bool = False
    is_observer: bool = False
    is_system: bool = False
    """
    Ruoli logici dell’agente.
    Usati per routing, policy e separazione delle responsabilità.
    """

    # ==================================================================
    # CAPACITÀ SEMANTICHE
    # ==================================================================

    capabilities: Set[str] = field(default_factory=set)
    """
    Capacità dichiarate, string-based.

    Esempi:
    - "code.read"
    - "code.write"
    - "knowledge.query"
    - "git.commit"
    - "log.analyze"

    NON sono enum per evitare coupling.
    """

    # ==================================================================
    # METADATA DI GOVERNANCE
    # ==================================================================

    version: Optional[str] = None
    """
    Versione cognitiva dell’agente.
    Cambia se cambia il comportamento dichiarato.
    """

    experimental: bool = False
    deprecated: bool = False

    # ==================================================================
    # PRESENTATION / UI HINTS
    # ==================================================================

    ui_label: Optional[str] = None
    ui_group: Optional[str] = None
    """
    Hint per UI / IDE / CLI.
    Non influenzano il routing.
    """

    # ==================================================================
    # SERIALIZZAZIONE
    # ==================================================================

    def to_dict(self) -> Dict[str, object]:
        """
        Rappresentazione serializzabile e stabile.
        """
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
            "governance": {
                "version": self.version,
                "experimental": self.experimental,
                "deprecated": self.deprecated,
            },
            "ui": {
                "label": self.ui_label,
                "group": self.ui_group,
            },
        }

    # ==================================================================
    # CONVENIENCE
    # ==================================================================

    def has_capability(self, capability: str) -> bool:
        return capability in self.capabilities
