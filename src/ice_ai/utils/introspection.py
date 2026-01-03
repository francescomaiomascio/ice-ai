from __future__ import annotations

from typing import Dict, Any

from ice_ai.agents.catalog import AGENT_CATALOG
from ice_ai.version import ICE_AI_VERSION


def introspect() -> Dict[str, Any]:
    """
    Restituisce una descrizione completa e statica di ICE-AI.

    Usata da:
    - engine
    - orchestrator
    - UI
    - debug / diagnostics
    """

    return {
        "version": ICE_AI_VERSION,
        "agents": {
            name: spec.to_dict()
            for name, spec in AGENT_CATALOG.items()
        },
        "agent_count": len(AGENT_CATALOG),
        "capabilities": sorted({
            cap
            for spec in AGENT_CATALOG.values()
            for cap in spec.capabilities
        }),
    }
