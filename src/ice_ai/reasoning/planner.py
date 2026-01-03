from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------
# PLAN STEP (concetto puro)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class PlanStep:
    id: str
    title: str
    description: str
    type: str = "plan"
    agent_hint: Optional[str] = None
    payload: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "agent_hint": self.agent_hint,
            "payload": self.payload or {},
        }


# ---------------------------------------------------------------------
# PLANNER CORE LOGIC
# ---------------------------------------------------------------------

class Planner:
    """
    Logica pura di pianificazione.

    NON:
    - chiama LLM
    - conosce agenti runtime
    - esegue task

    FA:
    - normalizza output di reasoning
    - costruisce piani coerenti
    - applica fallback strutturali
    """

    @staticmethod
    def build_plan(
        *,
        goal: str,
        raw_actions: Optional[List[Any]] = None,
    ) -> List[PlanStep]:
        """
        Costruisce un piano strutturato a partire da output grezzo
        (tipicamente prodotto da un LLM o da un router).

        `raw_actions` può essere:
        - lista di dict
        - lista di stringhe
        - None
        """

        steps: List[PlanStep] = []

        if not raw_actions:
            return Planner._fallback_plan(goal)

        for idx, action in enumerate(raw_actions, start=1):
            if isinstance(action, dict):
                desc = str(action.get("description", "")).strip()
                title = action.get("title") or desc[:60] or f"Step {idx}"

                steps.append(
                    PlanStep(
                        id=f"step-{idx}",
                        title=title,
                        description=desc,
                        type=str(action.get("type", "plan")),
                        agent_hint=action.get("agent_hint") or action.get("agent"),
                        payload=action.get("payload") or {},
                    )
                )
            else:
                steps.append(
                    PlanStep(
                        id=f"step-{idx}",
                        title=f"Step {idx}",
                        description=str(action),
                        payload={},
                    )
                )

        return steps or Planner._fallback_plan(goal)

    # -----------------------------------------------------------------

    @staticmethod
    def _fallback_plan(goal: str) -> List[PlanStep]:
        """
        Fallback deterministico se non arriva nulla di valido.
        """
        return [
            PlanStep(
                id="fallback-1",
                title="Generic plan",
                description=(
                    "No structured plan was produced. "
                    "This fallback step was generated automatically."
                ),
                payload={"goal": goal},
            )
        ]
