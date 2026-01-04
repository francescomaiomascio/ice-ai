from __future__ import annotations

from typing import Any, Dict, List, Set

from ice_ai.agents.catalog import ICE_AI_CATALOG
from ice_ai.version import ICE_AI_VERSION


# ============================================================
# CORE INTROSPECTION API (PURE, DETERMINISTIC)
# ============================================================

def introspect() -> Dict[str, Any]:
    """
    Restituisce una descrizione completa, statica e deterministica di ICE-AI.

    ⚠️ NON istanzia agenti
    ⚠️ NON accede a runtime / engine
    ⚠️ NON dipende da sessioni o workspace
    """

    catalog = ICE_AI_CATALOG
    agents = catalog.all()

    return {
        "ice_ai": {
            "version": ICE_AI_VERSION,
            "agent_count": len(catalog),
        },
        "agents": {
            spec.name: spec.to_dict()
            for spec in agents
        },
        "indexes": {
            "domains": _index_domains(agents),
            "roles": _index_roles(agents),
            "capabilities": _index_capabilities(agents),
        },
    }


# ============================================================
# INDEX BUILDERS (PURE FUNCTIONS)
# ============================================================

def _index_domains(agents) -> Dict[str, List[str]]:
    """
    domain -> [agent_name, ...]
    """
    index: Dict[str, List[str]] = {}

    for spec in agents:
        for domain in spec.domains:
            index.setdefault(domain, []).append(spec.name)

    return {k: sorted(v) for k, v in index.items()}


def _index_roles(agents) -> Dict[str, List[str]]:
    """
    role -> [agent_name, ...]
    """
    roles = {
        "planner": [],
        "executor": [],
        "observer": [],
        "system": [],
    }

    for spec in agents:
        if spec.is_planner:
            roles["planner"].append(spec.name)
        if spec.is_executor:
            roles["executor"].append(spec.name)
        if spec.is_observer:
            roles["observer"].append(spec.name)
        if spec.is_system:
            roles["system"].append(spec.name)

    return {k: sorted(v) for k, v in roles.items()}


def _index_capabilities(agents) -> Dict[str, List[str]]:
    """
    capability -> [agent_name, ...]
    """
    index: Dict[str, Set[str]] = {}

    for spec in agents:
        for cap in spec.capabilities:
            index.setdefault(cap, set()).add(spec.name)

    return {k: sorted(v) for k, v in index.items()}


# ============================================================
# SINGLE-ENTRY HELPERS
# ============================================================

def describe_agent(name: str) -> Dict[str, Any]:
    """
    Restituisce la descrizione serializzata di un singolo agente.
    """
    spec = ICE_AI_CATALOG.get(name)
    return spec.to_dict()


def describe_catalog() -> Dict[str, Any]:
    """
    Restituisce la descrizione completa del catalogo agenti.
    """
    return ICE_AI_CATALOG.to_dict()
