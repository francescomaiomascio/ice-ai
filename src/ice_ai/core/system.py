from __future__ import annotations

from typing import Dict, Any

from ice_ai.agents.spec import AgentSpec


class SystemAgent:
    """
    SystemAgent (CORE)

    Responsabilità:
    - stato globale ICE-AI
    - lifecycle hooks
    - introspezione runtime
    """

    spec = AgentSpec(
        name="system",
        description="Global system agent for lifecycle and global state.",
        domains={"system"},
        is_system=True,
        is_observer=True,
        capabilities={
            "lifecycle.read",
            "lifecycle.status",
            "system.introspect",
        },
        ui_label="System",
        ui_group="core",
    )

    def __init__(self):
        self._state: Dict[str, Any] = {
            "status": "initialized",
            "version": None,
        }

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def get_state(self) -> Dict[str, Any]:
        return dict(self._state)

    def set_state(self, key: str, value: Any) -> None:
        self._state[key] = value

    def introspect(self) -> Dict[str, Any]:
        """
        Espone stato minimo per UI / debug.
        """
        return {
            "agent": self.spec.name,
            "domains": list(self.spec.domains),
            "state": self.get_state(),
        }
