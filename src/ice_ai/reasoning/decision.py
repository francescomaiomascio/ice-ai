from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .routing import Intent, RoutingDecision


# =============================================================================
# DECISION CONTEXT
# =============================================================================

@dataclass(frozen=True)
class DecisionContext:
    """
    Contesto cognitivo minimo per una decisione.

    NON è runtime.
    NON è sessione.
    NON è workspace.

    Serve a valutare:
    - intenzione dell'utente
    - stato del sistema
    - segnali cognitivi
    """

    user_intent: Optional[str] = None
    """
    Intento espresso o inferito dall'utente (raw).
    """

    mode: Optional[str] = None
    """
    Modalità esplicita (plan, analyze, validate, ecc.).
    """

    lifecycle_state: Optional[str] = None
    """
    Stato logico del sistema (es. idle, planning, executing).
    """

    signals: Dict[str, Any] = field(default_factory=dict)
    """
    Segnali cognitivi:
    - error_count
    - uncertainty
    - llm_confidence
    - time_pressure
    ecc.
    """


# =============================================================================
# DECISION OUTPUT
# =============================================================================

@dataclass(frozen=True)
class Decision:
    """
    Esito di una decisione cognitiva.

    NON è un'azione.
    NON è un task.
    È una direttiva logica per il sistema.
    """

    intent: Intent
    """
    Intento finale accettato dal sistema.
    """

    proceed: bool
    """
    Se il sistema deve procedere con questo intent
    oppure fermarsi / chiedere chiarimenti.
    """

    reason: str
    """
    Motivazione della decisione.
    """

    confidence: float = 1.0
    """
    Affidabilità della decisione (0.0 – 1.0).
    """

    meta: Dict[str, Any] = field(default_factory=dict)
    """
    Metadati utili (vincoli, note, fallback).
    """


# =============================================================================
# DECISION POLICY (ABSTRACT)
# =============================================================================

class DecisionPolicy:
    """
    Policy astratta di decisione cognitiva.

    Una policy:
    - riceve una RoutingDecision
    - valuta il contesto
    - decide se procedere, bloccare o deviare
    """

    def decide(
        self,
        *,
        routing: RoutingDecision,
        context: DecisionContext,
    ) -> Decision:
        """
        Valuta una RoutingDecision alla luce del contesto.

        NON esegue nulla.
        NON muta stato.
        """
        raise NotImplementedError


# =============================================================================
# DEFAULT POLICY (SAFE)
# =============================================================================

class DefaultDecisionPolicy(DecisionPolicy):
    """
    Policy di default:
    - accetta quasi sempre
    - applica solo guardrail minimi
    """

    def decide(
        self,
        *,
        routing: RoutingDecision,
        context: DecisionContext,
    ) -> Decision:

        # -------------------------------------------------------------
        # BLOCCO: confidence troppo bassa
        # -------------------------------------------------------------
        if routing.confidence < 0.2:
            return Decision(
                intent=routing.intent,
                proceed=False,
                reason="Routing confidence too low.",
                confidence=routing.confidence,
                meta={"action": "ask_clarification"},
            )

        # -------------------------------------------------------------
        # BLOCCO: stato incompatibile
        # -------------------------------------------------------------
        if (
            context.lifecycle_state == "executing"
            and routing.intent == Intent.PLAN
        ):
            return Decision(
                intent=routing.intent,
                proceed=False,
                reason="Cannot plan while execution is in progress.",
                confidence=0.6,
                meta={"action": "wait"},
            )

        # -------------------------------------------------------------
        # DEFAULT: accetta
        # -------------------------------------------------------------
        return Decision(
            intent=routing.intent,
            proceed=True,
            reason="Decision accepted by default policy.",
            confidence=routing.confidence,
            meta={
                "suggested_roles": routing.suggested_roles,
                "payload": routing.payload,
            },
        )
