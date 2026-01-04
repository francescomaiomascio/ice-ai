from __future__ import annotations

"""
Cognitive Lifecycle — ICE-AI

Descrive le fasi cognitive di un agente ICE-AI.

⚠️ NON è lifecycle runtime
⚠️ NON è stato tecnico
⚠️ NON gestisce sessioni o workspace

Serve per:
- governance cognitiva
- routing
- prompt conditioning
- decision policy
- introspezione
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


# ---------------------------------------------------------------------
# LIFECYCLE STATES
# ---------------------------------------------------------------------

class LifecycleState(str, Enum):
    """
    Stato cognitivo globale dell'agente.

    Ogni stato impone:
    - vincoli di comportamento
    - limiti decisionali
    - aspettative di output
    """

    BOOT = "boot"
    """
    Sistema in inizializzazione.
    - Nessuna assunzione
    - Nessuna azione distruttiva
    - Preferire chiarimenti
    """

    IDLE = "idle"
    """
    Sistema in attesa di intenzione.
    - Non anticipare
    - Non pianificare senza richiesta
    """

    ACTIVE = "active"
    """
    Sistema impegnato in reasoning o task.
    - Agire secondo ruolo e capability
    - Applicare policy
    """

    CLOSING = "closing"
    """
    Fase finale.
    - Riassumere
    - Verificare coerenza
    - Non introdurre nuove azioni
    """

    ERROR = "error"
    """
    Stato di errore cognitivo.
    - Minimizzare output
    - Spiegare il problema
    - Proporre recovery
    """


# ---------------------------------------------------------------------
# LIFECYCLE DESCRIPTOR
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class LifecycleDescriptor:
    """
    Descrizione semantica di uno stato di lifecycle.

    Usata per:
    - prompt
    - introspezione
    - policy
    """

    state: LifecycleState
    description: str

    # vincoli cognitivi
    allow_planning: bool = False
    allow_execution: bool = False
    allow_decision: bool = False

    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "state": self.state.value,
            "description": self.description,
            "permissions": {
                "planning": self.allow_planning,
                "execution": self.allow_execution,
                "decision": self.allow_decision,
            },
            "notes": self.notes,
        }


# ---------------------------------------------------------------------
# CANONICAL LIFECYCLE REGISTRY
# ---------------------------------------------------------------------

LIFECYCLE_REGISTRY: Dict[LifecycleState, LifecycleDescriptor] = {
    LifecycleState.BOOT: LifecycleDescriptor(
        state=LifecycleState.BOOT,
        description="System initialization phase.",
        allow_planning=False,
        allow_execution=False,
        allow_decision=False,
        notes="Avoid assumptions and irreversible actions.",
    ),

    LifecycleState.IDLE: LifecycleDescriptor(
        state=LifecycleState.IDLE,
        description="Awaiting user intent.",
        allow_planning=False,
        allow_execution=False,
        allow_decision=False,
        notes="Wait for explicit intent.",
    ),

    LifecycleState.ACTIVE: LifecycleDescriptor(
        state=LifecycleState.ACTIVE,
        description="Active reasoning or task execution.",
        allow_planning=True,
        allow_execution=True,
        allow_decision=True,
        notes="Apply role, capabilities, and policy constraints.",
    ),

    LifecycleState.CLOSING: LifecycleDescriptor(
        state=LifecycleState.CLOSING,
        description="Finalization phase.",
        allow_planning=False,
        allow_execution=False,
        allow_decision=False,
        notes="Summarize and ensure consistency only.",
    ),

    LifecycleState.ERROR: LifecycleDescriptor(
        state=LifecycleState.ERROR,
        description="Cognitive error state.",
        allow_planning=False,
        allow_execution=False,
        allow_decision=False,
        notes="Explain error and suggest recovery.",
    ),
}
