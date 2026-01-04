from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

from ice_ai.agents.spec import AgentSpec
from ice_ai.agents.capabilities import Capability


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class ProjectIntent:
    """
    Rappresenta l'intento di alto livello di un progetto.
    È un input semantico, NON operativo.
    """
    goal: str
    constraints: Dict[str, Any]
    context: Dict[str, Any]


# ============================================================================
# AGENT
# ============================================================================

class ProjectAgent:
    """
    ProjectAgent
    ------------

    Domain-level project planner.
    Produces a ProjectIntent → ProjectPlan mapping contract.
    """

    spec = AgentSpec(
        name="project-agent",
        description="Defines high-level project planning intent.",
        domains={"workflow", "project"},
        is_planner=True,
        is_executor=False,
        is_observer=False,
        is_system=False,
        capabilities={
            Capability.WORKFLOW_PLAN,
            Capability.PROJECT_GENERATE,
        },
        ui_label="Project Planner",
        ui_group="Planning",
    )

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def plan_intent(
        self,
        goal: str,
        *,
        constraints: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ProjectIntent:
        """
        Produce a pure ProjectIntent.
        NO planning logic is executed here.
        """

        return ProjectIntent(
            goal=goal.strip(),
            constraints=constraints or {},
            context=context or {},
        )
