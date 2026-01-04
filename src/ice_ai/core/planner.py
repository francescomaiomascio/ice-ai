from __future__ import annotations

from typing import Dict, Any, List

from ice_ai.agents.spec import AgentSpec


class PlannerAgent:
    """
    PlannerAgent (CORE)

    Genera piani astratti e dichiarativi.
    NON esegue azioni.
    """

    spec = AgentSpec(
        name="planner",
        description="High-level planner that generates abstract workflows.",
        domains={"workflow"},
        is_planner=True,
        capabilities={
            "workflow.plan",
            "workflow.decompose",
        },
        ui_label="Planner",
        ui_group="core",
    )

    def plan(
        self,
        goal: str,
        context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Ritorna un piano dichiarativo minimale.

        Questo è VOLUTAMENTE semplice:
        la logica avanzata vivrà in reasoning/.
        """
        context = context or {}

        steps: List[Dict[str, Any]] = [
            {
                "id": "step-1",
                "type": "analysis",
                "title": "Analyze goal",
                "description": f"Analyze the goal: {goal}",
            },
            {
                "id": "step-2",
                "type": "execution",
                "title": "Execute workflow",
                "description": "Execute planned actions.",
            },
        ]

        return {
            "goal": goal,
            "context": context,
            "steps": steps,
        }
