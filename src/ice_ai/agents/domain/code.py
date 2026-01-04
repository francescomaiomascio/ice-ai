from __future__ import annotations

from typing import Dict, Any, List, Optional
from pathlib import Path

from ice_ai.agents.spec import AgentSpec


class CodeAgent:
    """
    CodeAgent (DOMAIN)

    Responsabilità:
    - lettura file
    - scrittura file
    - introspezione filesystem
    - operazioni di codice dichiarative (NO orchestrazione)
    - supporto a codegen / refactor tramite LLM o CodeModel (futuro)

    NON:
    - decide workflow
    - non gestisce lifecycle
    - non parla direttamente con IDE
    """

    spec = AgentSpec(
        name="code",
        description="Filesystem and code manipulation agent.",
        domains={"code"},
        is_executor=True,
        is_observer=True,
        capabilities={
            # filesystem
            "fs.read",
            "fs.write",
            "fs.exists",
            "fs.list",

            # code operations
            "code.generate",
            "code.refactor",
            "code.explain",
        },
        ui_label="Code",
        ui_group="domain",
    )

    # ------------------------------------------------------------------
    # FILESYSTEM
    # ------------------------------------------------------------------

    def read_file(self, path: str) -> Dict[str, Any]:
        p = Path(path)

        if not p.exists():
            return {"ok": False, "error": "file_not_found", "path": path}

        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            return {
                "ok": False,
                "error": "read_error",
                "path": path,
                "detail": str(exc),
            }

        return {
            "ok": True,
            "path": path,
            "content": content,
            "length": len(content),
        }

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        p = Path(path)

        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        except Exception as exc:
            return {
                "ok": False,
                "error": "write_error",
                "path": path,
                "detail": str(exc),
            }

        return {
            "ok": True,
            "path": path,
            "written": True,
            "bytes": len(content.encode("utf-8")),
        }

    def exists(self, path: str) -> Dict[str, Any]:
        return {
            "ok": True,
            "path": path,
            "exists": Path(path).exists(),
        }

    def list_dir(self, path: str) -> Dict[str, Any]:
        p = Path(path)

        if not p.exists() or not p.is_dir():
            return {
                "ok": False,
                "error": "not_a_directory",
                "path": path,
            }

        entries = []
        for e in p.iterdir():
            entries.append(
                {
                    "name": e.name,
                    "type": "dir" if e.is_dir() else "file",
                }
            )

        return {
            "ok": True,
            "path": path,
            "entries": entries,
        }

    # ------------------------------------------------------------------
    # CODE OPERATIONS (DECLARATIVE)
    # ------------------------------------------------------------------

    def generate_code(
        self,
        instruction: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Placeholder dichiarativo.
        Il backend reale verrà agganciato via llm.adapter o codemodel.
        """
        header = f"# Generated code\n# Instruction: {instruction}\n"
        if language:
            header += f"# Language: {language}\n"

        return {
            "ok": True,
            "output": header,
            "note": "code generation stub (no LLM attached)",
        }

    def refactor_code(
        self,
        code: str,
        goal: str,
    ) -> Dict[str, Any]:
        """
        Refactor dichiarativo (stub).
        """
        return {
            "ok": True,
            "goal": goal,
            "original_length": len(code),
            "proposed_code": f"# Refactor goal: {goal}\n{code}",
            "note": "refactor stub (no LLM attached)",
        }

    def explain_code(
        self,
        code: str,
    ) -> Dict[str, Any]:
        return {
            "ok": True,
            "length": len(code),
            "explanation": "Code explanation not available (stub).",
        }
