from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime

from ice_ai.agents.spec import AgentSpec
from ice_ai.agents.capabilities import CAP_HISTORY, CAP_REASONING


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass(frozen=True)
class HistoryEvent:
    """
    Evento normalizzato nella timeline cognitiva.
    """
    timestamp: str
    agent: str
    type: str
    message: str
    metadata: Dict[str, Any]


@dataclass
class Timeline:
    """
    Timeline semantica ordinata.
    """
    events: List[HistoryEvent]

    def slice(self, limit: int = 50) -> List[HistoryEvent]:
        return self.events[-limit:]


# ============================================================================
# AGENT
# ============================================================================

class HistorianAgent:
    """
    HistorianAgent
    --------------

    Responsabilità:
    - raccogliere eventi agent-level
    - normalizzarli temporalmente
    - fornire memoria storica semantica

    NON:
    - persiste
    - sincronizza
    - esporta
    """

    spec = AgentSpec(
        name="historian-agent",
        description="Agente di memoria temporale e reasoning storico.",
        domains={"knowledge"},
        is_planner=False,
        is_executor=False,
        is_observer=True,
        is_system=False,
        capabilities={
            CAP_HISTORY,
            CAP_REASONING,
        },
        ui_label="History",
        ui_group="Cognition",
    )

    # ------------------------------------------------------------------
    # INIT
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        self._timeline: List[HistoryEvent] = []

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def record(
        self,
        *,
        agent: str,
        type: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> HistoryEvent:
        """
        Registra un evento nella timeline cognitiva.
        """

        event = HistoryEvent(
            timestamp=datetime.utcnow().isoformat(),
            agent=agent,
            type=type,
            message=message,
            metadata=metadata or {},
        )

        self._timeline.append(event)
        return event

    def timeline(self, limit: int = 100) -> Timeline:
        """
        Restituisce la timeline ordinata (slice finale).
        """
        return Timeline(events=self._timeline[-limit:])

    def summarize(self, limit: int = 20) -> str:
        """
        Produce una sintesi semantica della timeline recente.
        """
        events = self._timeline[-limit:]
        if not events:
            return "Nessun evento registrato."

        lines = []
        for ev in events:
            lines.append(
                f"[{ev.timestamp}] ({ev.agent}) {ev.type}: {ev.message}"
            )

        return "\n".join(lines)
