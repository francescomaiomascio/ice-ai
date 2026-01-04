from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from ice_ai.agents.spec import AgentSpec
from ice_ai.agents.capabilities import CAP_PLANNING, CAP_PROJECT
from ice_ai.reasoning.planner import build_project_plan


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


@dataclass
class ProjectPlan:
    """
    Piano di progetto normalizzato e serializzabile.
    """
    goal: str
    steps: List[Dict[str, Any]]
    assumptions: List[str]
    risks: List[str]


# ============================================================================
# AGENT
# ============================================================================

class ProjectAgent:
    """
    ProjectAgent
    ------------

    Responsabilità:
    - trasformare un goal in un ProjectPlan
    - NON eseguire
    - NON scrivere codice
    - NON chiamare filesystem o runtime

    È un *domain planner*, non un orchestratore.
    """

    spec = AgentSpec(
        name="project-agent",
        description="Genera piani di progetto ad alto livello a partire da un goal.",
        domains={"workflow", "project"},
        is_planner=True,
        is_executor=False,
        is_observer=False,
        is_system=False,
        capabilities={
            CAP_PLANNING,
            CAP_PROJECT,
        },
        ui_label="Project Planner",
        ui_group="Planning",
    )

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def plan(
        self,
        goal: str,
        *,
        constraints: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ProjectPlan:
        """
        Genera un piano di progetto strutturato.
        """

        intent = ProjectIntent(
            goal=goal.strip(),
            constraints=constraints or {},
            context=context or {},
        )

        raw_plan = build_project_plan(intent)

        return ProjectPlan(
            goal=intent.goal,
            steps=raw_plan.get("steps", []),
            assumptions=raw_plan.get("assumptions", []),
            risks=raw_plan.get("risks", []),
        )
