from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =====================================================================
# PLAN STEP (COGNITIVE UNIT)
# =====================================================================

@dataclass(frozen=True)
class PlanStep:
    """
    Singolo step logico di un piano cognitivo.

    NON è:
    - un task runtime
    - un'azione eseguibile
    - un binding ad un agente reale

    È una direttiva semantica.
    """

    id: str
    title: str
    description: str

    # tipo concettuale dello step (plan / analyze / validate / refactor / ecc.)
    type: str = "plan"

    # hint opzionale per il routing (nome agente o ruolo)
    agent_hint: Optional[str] = None

    # payload cognitivo (mai mutato runtime)
    payload: Dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "agent_hint": self.agent_hint,
            "payload": dict(self.payload),
        }


# =====================================================================
# PLANNER (PURE LOGIC)
# =====================================================================

class Planner:
    """
    Planner cognitivo puro.

    RESPONSABILITÀ:
    - trasformare output grezzo (LLM / router) in piano coerente
    - applicare fallback deterministici
    - garantire struttura stabile

    NON FA:
    - chiamate LLM
    - routing runtime
    - scheduling
    """

    # -------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------

    @staticmethod
    def build_plan(
        *,
        goal: str,
        raw_actions: Optional[List[Any]] = None,
    ) -> List[PlanStep]:
        """
        Costruisce un piano strutturato a partire da input grezzo.

        raw_actions può essere:
        - None
        - lista di dict
        - lista di stringhe
        - mix inconsistente (gestito)
        """

        if not raw_actions:
            return Planner._fallback_plan(goal)

        steps: List[PlanStep] = []

        for idx, action in enumerate(raw_actions, start=1):
            step = Planner._normalize_action(
                action=action,
                index=idx,
            )
            if step:
                steps.append(step)

        return steps or Planner._fallback_plan(goal)

    # -------------------------------------------------------------
    # NORMALIZATION
    # -------------------------------------------------------------

    @staticmethod
    def _normalize_action(
        *,
        action: Any,
        index: int,
    ) -> Optional[PlanStep]:
        """
        Normalizza una singola azione grezza in PlanStep.

        Ritorna None se l'azione è inutilizzabile.
        """

        step_id = f"step-{index}"

        # -------------------------------
        # CASE 1: dict strutturato
        # -------------------------------
        if isinstance(action, dict):
            description = str(action.get("description") or "").strip()
            title = (
                action.get("title")
                or description[:64]
                or f"Step {index}"
            )

            return PlanStep(
                id=step_id,
                title=title,
                description=description or title,
                type=str(action.get("type", "plan")),
                agent_hint=action.get("agent_hint") or action.get("agent"),
                payload=dict(action.get("payload") or {}),
            )

        # -------------------------------
        # CASE 2: string / fallback
        # -------------------------------
        if isinstance(action, str):
            text = action.strip()
            if not text:
                return None

            return PlanStep(
                id=step_id,
                title=f"Step {index}",
                description=text,
            )

        # -------------------------------
        # CASE 3: ignoto → scartato
        # -------------------------------
        return None

    # -------------------------------------------------------------
    # FALLBACK
    # -------------------------------------------------------------

    @staticmethod
    def _fallback_plan(goal: str) -> List[PlanStep]:
        """
        Piano minimo deterministico se non arriva nulla di valido.
        """
        return [
            PlanStep(
                id="fallback-1",
                title="Generic planning step",
                description=(
                    "No structured plan was produced. "
                    "This fallback step was generated automatically."
                ),
                payload={"goal": goal},
            )
        ]
