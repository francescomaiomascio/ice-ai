from __future__ import annotations

import ast
from typing import Dict, Any, List, Optional

from ice_ai.agents.spec import AgentSpec


class ValidatorAgent:
    """
    ValidatorAgent (DOMAIN)

    Responsabilità:
    - validazione sintattica (AST)
    - validazione semantica light (rule-based)
    - preparazione contesto per LLM (opzionale, esterno)

    NON:
    - modifica codice
    - applica fix
    - prende decisioni
    """

    spec = AgentSpec(
        name="validator",
        description="Code validation (syntax + semantic signals).",
        domains={"code"},
        is_observer=True,
        capabilities={
            "code.validate.syntax",
            "code.validate.semantic",
        },
        ui_label="Validator",
        ui_group="domain",
    )

    # ------------------------------------------------------------------
    # API PUBBLICA
    # ------------------------------------------------------------------

    def validate(
        self,
        code: str,
        filename: Optional[str] = None,
        goal: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Valida codice Python.

        Ritorna sempre un report strutturato.
        """
        if not code.strip():
            return self._error(
                "empty_code",
                "No code provided for validation.",
                filename,
            )

        issues: List[Dict[str, Any]] = []

        # 1) SINTASSI
        syntax_issues = self._validate_syntax(code)
        issues.extend(syntax_issues)

        if any(i["severity"] == "error" for i in issues):
            return self._result(
                ok=False,
                issues=issues,
                filename=filename,
                goal=goal,
            )

        # 2) SEMANTICA BASE (rule-based)
        semantic_issues = self._validate_semantic(code)
        issues.extend(semantic_issues)

        ok = not any(i["severity"] in {"error", "warning"} for i in issues)

        return self._result(
            ok=ok,
            issues=issues,
            filename=filename,
            goal=goal,
        )

    # ------------------------------------------------------------------
    # VALIDATION STEPS
    # ------------------------------------------------------------------

    def _validate_syntax(self, code: str) -> List[Dict[str, Any]]:
        try:
            ast.parse(code)
            return []
        except SyntaxError as e:
            return [
                {
                    "type": "syntax",
                    "severity": "error",
                    "message": str(e),
                    "line": e.lineno,
                    "column": e.offset,
                }
            ]

    def _validate_semantic(self, code: str) -> List[Dict[str, Any]]:
        """
        Heuristiche semplici, deterministic, NO LLM.
        """
        issues: List[Dict[str, Any]] = []

        if "print(" in code:
            issues.append(
                {
                    "type": "style",
                    "severity": "warning",
                    "message": "Usage of print() detected (consider logging).",
                }
            )

        if "TODO" in code or "FIXME" in code:
            issues.append(
                {
                    "type": "maintainability",
                    "severity": "info",
                    "message": "TODO/FIXME markers found in code.",
                }
            )

        return issues

    # ------------------------------------------------------------------
    # RESULT BUILDERS
    # ------------------------------------------------------------------

    def _result(
        self,
        ok: bool,
        issues: List[Dict[str, Any]],
        filename: Optional[str],
        goal: Optional[str],
    ) -> Dict[str, Any]:
        return {
            "ok": ok,
            "filename": filename,
            "goal": goal,
            "issues": issues,
            "summary": self._summarize(issues),
        }

    def _error(
        self,
        code: str,
        message: str,
        filename: Optional[str],
    ) -> Dict[str, Any]:
        return {
            "ok": False,
            "filename": filename,
            "error": code,
            "message": message,
            "issues": [],
        }

    def _summarize(self, issues: List[Dict[str, Any]]) -> str:
        if not issues:
            return "No issues detected."

        errors = sum(1 for i in issues if i["severity"] == "error")
        warnings = sum(1 for i in issues if i["severity"] == "warning")

        parts = []
        if errors:
            parts.append(f"{errors} error(s)")
        if warnings:
            parts.append(f"{warnings} warning(s)")

        return "Validation completed with " + ", ".join(parts)
