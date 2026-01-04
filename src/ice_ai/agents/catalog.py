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

from ice_ai.agents.capabilities import Capability
from ice_ai.agents.spec import AgentSpec


# =====================================================================
# AGENT CATALOG
# =====================================================================

class AgentCatalog:
    """
    Catalogo immutabile di AgentSpec.
    """

    def __init__(self, agents: Iterable[AgentSpec]) -> None:
        registry: Dict[str, AgentSpec] = {}

        for spec in agents:
            if spec.name in registry:
                raise ValueError(
                    f"Duplicate AgentSpec name detected: {spec.name}"
                )
            registry[spec.name] = spec

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
        return [s for s in self._agents.values() if domain in s.domains]

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

    def __len__(self) -> int:  # pragma: no cover
        return len(self._agents)

    def __iter__(self):  # pragma: no cover
        return iter(self.all())

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AgentCatalog agents={len(self._agents)}>"


# =====================================================================
# CANONICAL ICE-AI CATALOG
# =====================================================================

SYSTEM_SPEC = AgentSpec(
    name="system",
    description="Global ICE-AI system agent.",
    domains={"system"},
    is_system=True,
    is_observer=True,
    capabilities={Capability.SYSTEM_INTROSPECT},
)

CODE_SPEC = AgentSpec(
    name="code",
    description="Filesystem and code manipulation agent.",
    domains={"code"},
    is_executor=True,
    is_observer=True,
    capabilities={
        Capability.CODE_READ,
        Capability.CODE_WRITE,
        Capability.CODE_GENERATE,
        Capability.CODE_REFACTOR,
    },
)

KNOWLEDGE_SPEC = AgentSpec(
    name="knowledge",
    description="Knowledge base and RAG agent.",
    domains={"knowledge"},
    is_observer=True,
    capabilities={
        Capability.KNOWLEDGE_QUERY,
        Capability.RAG_QUERY,
        Capability.KNOWLEDGE_SYNC,
    },
)

ICE_AI_CATALOG = AgentCatalog([
    SYSTEM_SPEC,
    CODE_SPEC,
    KNOWLEDGE_SPEC,
])
