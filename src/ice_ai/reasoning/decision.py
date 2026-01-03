from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------
# DECISION CONTEXT
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class DecisionContext:
    """
    Contesto cognitivo minimo per una decisione.

    NON è runtime.
    NON è sessione.
    NON è workspace.

    Serve per valutare:
    - intenzione
    - stato
    - vincoli
    """

    user_intent: Optional[str] = None
    mode: Optional[str] = None
    lifecycle_state: Optional[str] = None
    signals: Dict[str, Any] = None


# ---------------------------------------------------------------------
# DECISION OUTPUT
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Decision:
    """
    Esito di una decisione cognitiva.

    NON è un'azione.
    NON è un task.
    È una direttiva logica.
    """

    kind: str
    reason: str
    confidence: Optional[float] = None
    meta: Dict[str, Any] = None


# ---------------------------------------------------------------------
# DECISION POLICY (ABSTRACT)
# ---------------------------------------------------------------------

class DecisionPolicy:
    """
    Policy astratta di decisione.

    Implementazioni future:
    - rule-based
    - heuristic
    - LLM-assisted
    - hybrid
    """

    def decide(
        self,
        context: DecisionContext,
        *,
        routing_hint: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Decision:
        """
        Valuta il contesto e produce una decisione.

        NON esegue nulla.
        NON muta stato.
        """
        raise NotImplementedError("DecisionPolicy.decide() not implemented")
