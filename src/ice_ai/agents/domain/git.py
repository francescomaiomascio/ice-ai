from __future__ import annotations

import subprocess
from typing import Dict, Any, List, Optional

from ice_ai.agents.spec import AgentSpec


class GitAgent:
    """
    GitAgent (DOMAIN)

    Responsabilità:
    - interrogare repository Git
    - produrre stato, diff, log, branch
    - eseguire commit / checkout in modo esplicito

    NON:
    - orchestrare workflow
    - decidere policy
    - parlare con UI o IDE
    """

    spec = AgentSpec(
        name="git",
        description="Git repository inspection and operations.",
        domains={"code"},
        is_executor=True,
        is_observer=True,
        capabilities={
            "git.status",
            "git.diff",
            "git.log",
            "git.commit",
            "git.checkout",
            "git.branches",
        },
        ui_label="Git",
        ui_group="domain",
    )

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------

    def _run(
        self,
        repo: str,
        args: List[str],
    ) -> Dict[str, Any]:
        try:
            proc = subprocess.run(
                ["git"] + args,
                cwd=repo,
                capture_output=True,
                text=True,
            )
        except Exception as exc:
            return {
                "ok": False,
                "error": "git_execution_failed",
                "detail": str(exc),
            }

        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "returncode": proc.returncode,
            "command": "git " + " ".join(args),
        }

    # ------------------------------------------------------------------
    # READ OPERATIONS
    # ------------------------------------------------------------------

    def status(self, repo: str) -> Dict[str, Any]:
        res = self._run(repo, ["status", "--porcelain=v1"])
        if not res.get("ok"):
            return res

        lines = res["stdout"].splitlines() if res["stdout"] else []

        return {
            "ok": True,
            "repo": repo,
            "changed_files": lines,
            "count": len(lines),
        }

    def diff(self, repo: str, path: Optional[str] = None) -> Dict[str, Any]:
        args = ["diff"]
        if path:
            args.append(path)

        res = self._run(repo, args)
        if not res.get("ok"):
            return res

        return {
            "ok": True,
            "repo": repo,
            "path": path,
            "diff": res["stdout"],
        }

    def log(self, repo: str, limit: int = 10) -> Dict[str, Any]:
        res = self._run(
            repo,
            ["log", f"-{limit}", "--pretty=format:%h|%an|%ad|%s"],
        )
        if not res.get("ok"):
            return res

        entries = []
        for line in res["stdout"].splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                entries.append(
                    {
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3],
                    }
                )

        return {
            "ok": True,
            "repo": repo,
            "entries": entries,
            "count": len(entries),
        }

    def branches(self, repo: str) -> Dict[str, Any]:
        res = self._run(repo, ["branch", "--all"])
        if not res.get("ok"):
            return res

        branches = [
            line.replace("*", "").strip()
            for line in res["stdout"].splitlines()
        ]

        return {
            "ok": True,
            "repo": repo,
            "branches": branches,
            "count": len(branches),
        }

    # ------------------------------------------------------------------
    # WRITE OPERATIONS
    # ------------------------------------------------------------------

    def commit(self, repo: str, message: str) -> Dict[str, Any]:
        add = self._run(repo, ["add", "-A"])
        if not add.get("ok"):
            return add

        commit = self._run(repo, ["commit", "-m", message])
        if not commit.get("ok"):
            return commit

        return {
            "ok": True,
            "repo": repo,
            "message": message,
            "stdout": commit.get("stdout"),
        }

    def checkout(self, repo: str, branch: str) -> Dict[str, Any]:
        res = self._run(repo, ["checkout", branch])
        if not res.get("ok"):
            return res

        return {
            "ok": True,
            "repo": repo,
            "branch": branch,
            "stdout": res.get("stdout"),
        }
