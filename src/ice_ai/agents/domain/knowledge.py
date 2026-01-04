from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List

from ice_ai.agents.spec import AgentSpec
from ice_ai.agents.capabilities import Capability


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class KnowledgeQuery:
    """
    Query semantica verso la conoscenza.
    """
    query: str
    context: Dict[str, Any]
    sources: List[str]


@dataclass
class KnowledgeResponse:
    """
    Risposta knowledge-driven strutturata.
    """
    answer: str
    evidence: List[Dict[str, Any]]
    confidence: float
    gaps: List[str]


# ============================================================================
# AGENT
# ============================================================================

class KnowledgeAgent:
    """
    KnowledgeAgent
    --------------

    Responsabilità:
    - query conoscenza
    - RAG
    - sync knowledge

    NON:
    - prende decisioni
    - sintetizza output
    - coordina reasoning
    """

    spec = AgentSpec(
        name="knowledge",
        description="Knowledge base and RAG agent.",
        domains={"knowledge"},
        is_planner=False,
        is_executor=False,
        is_observer=True,
        is_system=False,
        capabilities={
            Capability.KNOWLEDGE_QUERY,
            Capability.RAG_QUERY,
            Capability.KNOWLEDGE_SYNC,
        },
        ui_label="Knowledge",
        ui_group="domain",
    )
