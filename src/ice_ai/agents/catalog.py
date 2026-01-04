from __future__ import annotations

"""
Agent Catalog — registro canonico degli agenti ICE-AI.

RESPONSABILITÀ:
- dichiarare quali agenti ESISTONO
- fornire introspezione stabile
- supportare planning / routing / UI / CLI

NON FA:
- istanziazione
- esecuzione
- import di agent runtime
- binding engine / LLM / filesystem
"""

from typing import Dict, Iterable, List

from .spec import AgentSpec


# =====================================================================
# AGENT CATALOG
# =====================================================================

class AgentCatalog:
    """
    Catalogo immutabile di AgentSpec.

    È il punto di verità per:
    - planner cognitivo
    - routing logico
    - UI / IDE / CLI
    - validazione orchestratore
    """

    def __init__(self, agents: Iterable[AgentSpec]) -> None:
        registry: Dict[str, AgentSpec] = {}

        for spec in agents:
            if spec.name in registry:
                raise ValueError(
                    f"Duplicate AgentSpec name detected: {spec.name}"
                )
            registry[spec.name] = spec

        # Stato congelato
        self._agents: Dict[str, AgentSpec] = dict(registry)

    # ------------------------------------------------------------------
    # LOOKUP
    # ------------------------------------------------------------------

    def get(self, name: str) -> AgentSpec:
        try:
            return self._agents[name]
        except KeyError:
            raise KeyError(f"Agent not found in catalog: {name}")

    def exists(self, name: str) -> bool:
        return name in self._agents

    # ------------------------------------------------------------------
    # ITERATION
    # ------------------------------------------------------------------

    def all(self) -> List[AgentSpec]:
        return list(sorted(self._agents.values(), key=lambda a: a.name))

    def names(self) -> List[str]:
        return sorted(self._agents.keys())

    # ------------------------------------------------------------------
    # FILTERING
    # ------------------------------------------------------------------

    def by_domain(self, domain: str) -> List[AgentSpec]:
        return [
            spec for spec in self._agents.values()
            if domain in spec.domains
        ]

    def planners(self) -> List[AgentSpec]:
        return [s for s in self._agents.values() if s.is_planner]

    def executors(self) -> List[AgentSpec]:
        return [s for s in self._agents.values() if s.is_executor]

    def observers(self) -> List[AgentSpec]:
        return [s for s in self._agents.values() if s.is_observer]

    def system_agents(self) -> List[AgentSpec]:
        return [s for s in self._agents.values() if s.is_system]

    # ------------------------------------------------------------------
    # INTROSPECTION
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, object]:
        return {
            "total_agents": len(self._agents),
            "agents": {
                name: spec.to_dict()
                for name, spec in self._agents.items()
            },
        }

    # ------------------------------------------------------------------

    def __len__(self) -> int:  # pragma: no cover
        return len(self._agents)

    def __iter__(self):  # pragma: no cover
        return iter(self.all())

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AgentCatalog agents={len(self._agents)}>"
