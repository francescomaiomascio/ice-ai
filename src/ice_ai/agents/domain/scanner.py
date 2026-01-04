from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from ice_ai.agents.spec import AgentSpec


class ScannerAgent:
    """
    ScannerAgent (DOMAIN)

    Responsabilità:
    - scansione filesystem
    - enumerazione file
    - metadata strutturata
    - preparazione input per Analyzer / Validator / Knowledge

    NON:
    - indicizza vettorialmente
    - modifica file
    - applica logica semantica
    """

    spec = AgentSpec(
        name="scanner",
        description="Filesystem scanner and project structure observer.",
        domains={"code", "filesystem"},
        is_observer=True,
        capabilities={
            "fs.scan",
            "fs.list",
            "fs.metadata",
        },
        ui_label="Scanner",
        ui_group="domain",
    )

    # ------------------------------------------------------------------
    # API PUBBLICA
    # ------------------------------------------------------------------

    def scan(
        self,
        root: str,
        patterns: Optional[List[str]] = None,
        recursive: bool = True,
    ) -> Dict[str, Any]:
        """
        Scansiona una directory e ritorna metadata strutturata.
        """
        root_path = Path(root).resolve()

        if not root_path.exists():
            return self._error(
                "root_not_found",
                f"Root path does not exist: {root_path}",
            )

        patterns = patterns or [".py", ".md", ".txt"]

        files: List[Dict[str, Any]] = []
        errors: List[str] = []

        for dirpath, _, filenames in os.walk(root_path):
            for name in filenames:
                if not self._match(name, patterns):
                    continue

                path = Path(dirpath) / name
                try:
                    files.append(self._describe_file(path))
                except Exception as e:
                    errors.append(f"{path}: {e}")

            if not recursive:
                break

        return {
            "root": str(root_path),
            "patterns": patterns,
            "recursive": recursive,
            "summary": {
                "files_found": len(files),
                "errors": len(errors),
            },
            "files": files,
            "errors": errors,
        }

    # ------------------------------------------------------------------
    # INTERNALS
    # ------------------------------------------------------------------

    def _match(self, filename: str, patterns: List[str]) -> bool:
        return any(filename.endswith(p) for p in patterns)

    def _describe_file(self, path: Path) -> Dict[str, Any]:
        stat = path.stat()

        return {
            "path": str(path),
            "name": path.name,
            "extension": path.suffix,
            "size": stat.st_size,
            "modified": int(stat.st_mtime),
            "type": self._classify(path),
        }

    def _classify(self, path: Path) -> str:
        if path.suffix == ".py":
            return "python"
        if path.suffix in {".md", ".rst"}:
            return "documentation"
        if path.suffix in {".json", ".yaml", ".yml"}:
            return "data"
        return "generic"

    def _error(self, code: str, message: str) -> Dict[str, Any]:
        return {
            "ok": False,
            "error": code,
            "message": message,
            "files": [],
        }
