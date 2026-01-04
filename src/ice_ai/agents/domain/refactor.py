from __future__ import annotations

import difflib
from typing import Dict, Any, Optional

from ice_ai.agents.spec import AgentSpec


class RefactorAgent:
    """
    RefactorAgent (DOMAIN)

    Responsabilità:
    - analizzare codice esistente
    - proporre refactor deterministici o LLM-driven
    - produrre diff strutturato
    - NON applica patch (decisione esterna)

    Output sempre dichiarativo.
    """

    spec = AgentSpec(
        name="refactor",
        description="Code refactoring proposal and diff generation.",
        domains={"code"},
        is_executor=True,
        is_observer=True,
        capabilities={
            "code.refactor.propose",
            "code.refactor.diff",
        },
        ui_label="Refactor",
        ui_group="domain",
    )

    # ------------------------------------------------------------------
    # API PUBBLICA
    # ------------------------------------------------------------------

    def propose(
        self,
        code: str,
        goal: str,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Produce una proposta di refactor.

        NON modifica nulla.
        NON assume applicazione automatica.
        """

        if not code.strip():
            return {
                "ok": False,
                "error": "empty_code",
                "message": "No code provided for refactor.",
            }

        # Placeholder deterministico (LLM verrà agganciato sopra)
        proposed_code = self._mock_refactor(code, goal)

        diff = self._build_diff(code, proposed_code)

        return {
            "ok": True,
            "goal": goal,
            "filename": filename,
            "summary": self._summarize(goal),
            "diff": diff,
            "before": code,
            "after": proposed_code,
            "actions": [],
        }

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------

    def _mock_refactor(self, code: str, goal: str) -> str:
        """
        Refactor placeholder.
        Serve a mantenere pipeline completa senza LLM.
        """
        header = f"# Refactor goal: {goal}\n"
        if code.lstrip().startswith("#"):
            return header + code
        return header + "\n" + code

    def _build_diff(self, before: str, after: str) -> str:
        lines = difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="before",
            tofile="after",
        )
        return "".join(lines)

    def _summarize(self, goal: str) -> str:
        return f"Refactor proposal generated for goal: {goal}"
