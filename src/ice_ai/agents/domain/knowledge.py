from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from ice_ai.agents.spec import AgentSpec
from ice_ai.agents.capabilities import CAP_KNOWLEDGE, CAP_REASONING
from ice_ai.reasoning.decision import synthesize_knowledge


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
    - ragionare su conoscenza esistente
    - fondere query + contesto + fonti
    - produrre risposte spiegabili

    NON:
    - indicizza
    - persiste
    - esegue query tecniche
    """

    spec = AgentSpec(
        name="knowledge-agent",
        description="Agente di reasoning knowledge-driven (RAG-agnostic).",
        domains={"knowledge"},
        is_planner=False,
        is_executor=False,
        is_observer=True,
        is_system=False,
        capabilities={
            CAP_KNOWLEDGE,
            CAP_REASONING,
        },
        ui_label="Knowledge",
        ui_group="Cognition",
    )

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def query(
        self,
        text: str,
        *,
        context: Optional[Dict[str, Any]] = None,
        sources: Optional[List[str]] = None,
    ) -> KnowledgeResponse:
        """
        Risponde a una query basata su conoscenza disponibile.
        """

        q = KnowledgeQuery(
            query=text.strip(),
            context=context or {},
            sources=sources or [],
        )

        result = synthesize_knowledge(
            query=q.query,
            context=q.context,
            sources=q.sources,
        )

        return KnowledgeResponse(
            answer=result.get("answer", ""),
            evidence=result.get("evidence", []),
            confidence=float(result.get("confidence", 0.0)),
            gaps=result.get("gaps", []),
        )
