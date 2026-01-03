from __future__ import annotations

"""
Agent Catalog — registro statico degli agenti ICE-AI.

RESPONSABILITÀ:
- dichiarare quali agenti ESISTONO
- fornire introspezione stabile
- supportare routing / planning / UI / CLI

NON FA:
- istanziazione
- esecuzione
- binding runtime
- dipendenze engine
"""

from typing import Dict, Iterable, List

from .spec import AgentSpec


class AgentCatalog:
    """
    Catalogo immutabile di AgentSpec.

    È il punto di verità per:
    - orchestrator logico
    - planner
    - routing LLM
    - UI / CLI / IDE
    """

    def __init__(self, agents: Iterable[AgentSpec]) -> None:
        registry: Dict[str, AgentSpec] = {}

        for agent in agents:
            if agent.name in registry:
                raise ValueError(
                    f"Duplicate AgentSpec name detected: {agent.name}"
                )
            registry[agent.name] = agent

        # congeliamo lo stato interno
        self._agents: Dict[str, AgentSpec] = dict(registry)

    # ------------------------------------------------------------------
    # LOOKUP
    # ------------------------------------------------------------------

    def get(self, name: str) -> AgentSpec:
        """Ritorna un AgentSpec per nome."""
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
        """Ritorna tutti gli agenti (ordine deterministico)."""
        return list(sorted(self._agents.values(), key=lambda a: a.name))

    def names(self) -> List[str]:
        return sorted(self._agents.keys())

    # ------------------------------------------------------------------
    # FILTERING
    # ------------------------------------------------------------------

    def by_domain(self, domain: str) -> List[AgentSpec]:
        return [
            a for a in self._agents.values()
            if domain in a.domains
        ]

    def planners(self) -> List[AgentSpec]:
        return [a for a in self._agents.values() if a.is_planner]

    def executors(self) -> List[AgentSpec]:
        return [a for a in self._agents.values() if a.is_executor]

    def observers(self) -> List[AgentSpec]:
        return [a for a in self._agents.values() if a.is_observer]

    def system_agents(self) -> List[AgentSpec]:
        return [a for a in self._agents.values() if a.is_system]

    # ------------------------------------------------------------------
    # INTROSPECTION
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, object]:
        """
        Snapshot serializzabile del catalogo.
        """
        return {
            "total_agents": len(self._agents),
            "agents": {
                name: agent.to_dict()
                for name, agent in self._agents.items()
            },
        }

    def __len__(self) -> int:  # pragma: no cover
        return len(self._agents)

    def __iter__(self):  # pragma: no cover
        return iter(self.all())

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AgentCatalog agents={len(self._agents)}>"
