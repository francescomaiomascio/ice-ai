from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


# =============================================================================
# INTENT
# =============================================================================

class Intent(str, Enum):
    """
    Intento cognitivo di alto livello.
    NON è un'azione runtime.
    """
    RESPOND = "respond"        # risposta diretta
    PLAN = "plan"              # costruzione workflow
    ANALYZE = "analyze"        # analisi (code, log, testo)
    VALIDATE = "validate"      # validazione / controllo
    OBSERVE = "observe"        # scan / indexing / logging
    SYNTHESIZE = "synthesize"  # sintesi / knowledge / historian
    EXECUTE = "execute"        # esecuzione concreta


# =============================================================================
# ROUTING DECISION
# =============================================================================

@dataclass(frozen=True)
class RoutingDecision:
    """
    Decisione cognitiva pura del sistema ICE-AI.

    Dice:
    - CHE TIPO DI PENSIERO serve
    - PERCHÉ
    - CON QUALI DATI
    - QUALI RUOLI sono adatti
    """

    intent: Intent
    reason: str

    payload: Dict[str, Any] = field(default_factory=dict)

    suggested_roles: List[str] = field(default_factory=list)
    """
    Ruoli logici suggeriti:
    - planner
    - analyzer
    - executor
    - observer
    - system
    """

    confidence: float = 1.0
    """
    Quanto è forte questa decisione (0.0 – 1.0).
    Utile per fallback o multi-routing.
    """


# =============================================================================
# ROUTER (PURE LOGIC)
# =============================================================================

class Router:
    """
    Router cognitivo puro.

    NON:
    - conosce agenti concreti
    - conosce runtime
    - istanzia nulla

    FA:
    - interpreta input + output LLM
    - produce una RoutingDecision
    """

    # -----------------------------------------------------------------
    # ENTRYPOINT
    # -----------------------------------------------------------------

    @staticmethod
    def route(
        *,
        user_query: str,
        llm_output: Optional[Dict[str, Any]] = None,
        mode: Optional[str] = None,
    ) -> RoutingDecision:
        """
        Determina il prossimo INTENT cognitivo.
        """

        llm_output = llm_output or {}

        # -------------------------------------------------------------
        # 1) MODE ESPLICITO (override umano / UI)
        # -------------------------------------------------------------

        if mode:
            return Router._route_by_mode(
                mode=mode,
                user_query=user_query,
                llm_output=llm_output,
            )

        # -------------------------------------------------------------
        # 2) SE LLM HA PRODOTTO AZIONI → PLAN
        # -------------------------------------------------------------

        if _has_actions(llm_output):
            return RoutingDecision(
                intent=Intent.PLAN,
                reason="Structured actions detected in model output.",
                payload={
                    "goal": user_query,
                    "actions": llm_output.get("actions"),
                },
                suggested_roles=["planner"],
                confidence=0.9,
            )

        # -------------------------------------------------------------
        # 3) SE CI SONO ISSUE / ERRORI → VALIDATE
        # -------------------------------------------------------------

        if _has_issues(llm_output):
            return RoutingDecision(
                intent=Intent.VALIDATE,
                reason="Potential issues or errors detected.",
                payload={
                    "issues": llm_output.get("issues"),
                },
                suggested_roles=["validator"],
                confidence=0.8,
            )

        # -------------------------------------------------------------
        # 4) SE OUTPUT È ANALITICO → ANALYZE
        # -------------------------------------------------------------

        if _looks_like_analysis(llm_output):
            return RoutingDecision(
                intent=Intent.ANALYZE,
                reason="Analytical content detected.",
                payload={
                    "content": llm_output,
                },
                suggested_roles=["analyzer"],
                confidence=0.6,
            )

        # -------------------------------------------------------------
        # 5) DEFAULT → RESPOND
        # -------------------------------------------------------------

        return RoutingDecision(
            intent=Intent.RESPOND,
            reason="No further cognitive processing required.",
            payload={
                "answer": llm_output.get("answer"),
            },
            suggested_roles=[],
            confidence=0.5,
        )

    # -----------------------------------------------------------------
    # MODE ROUTING
    # -----------------------------------------------------------------

    @staticmethod
    def _route_by_mode(
        *,
        mode: str,
        user_query: str,
        llm_output: Dict[str, Any],
    ) -> RoutingDecision:
        """
        Routing deterministico per mode esplicito.
        """

        if mode == "plan":
            return RoutingDecision(
                intent=Intent.PLAN,
                reason="Explicit planning mode requested.",
                payload={"goal": user_query},
                suggested_roles=["planner"],
                confidence=1.0,
            )

        if mode == "analyze":
            return RoutingDecision(
                intent=Intent.ANALYZE,
                reason="Explicit analysis mode requested.",
                payload={"content": user_query},
                suggested_roles=["analyzer"],
                confidence=1.0,
            )

        if mode == "validate":
            return RoutingDecision(
                intent=Intent.VALIDATE,
                reason="Explicit validation mode requested.",
                payload={"content": user_query},
                suggested_roles=["validator"],
                confidence=1.0,
            )

        return RoutingDecision(
            intent=Intent.RESPOND,
            reason=f"Unknown mode '{mode}', fallback to respond.",
            payload={"answer": llm_output.get("answer")},
            confidence=0.3,
        )


# =============================================================================
# HEURISTIC HELPERS (PURE)
# =============================================================================

def _has_actions(output: Dict[str, Any]) -> bool:
    actions = output.get("actions")
    return isinstance(actions, list) and len(actions) > 0


def _has_issues(output: Dict[str, Any]) -> bool:
    issues = output.get("issues")
    return isinstance(issues, list) and len(issues) > 0


def _looks_like_analysis(output: Dict[str, Any]) -> bool:
    return any(
        key in output
        for key in ("reasoning", "analysis", "thoughts", "insight")
    )
