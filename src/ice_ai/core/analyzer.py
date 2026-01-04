from __future__ import annotations

from typing import Dict, Any

from ice_ai.agents.spec import AgentSpec


class AnalyzerAgent:
    """
    AnalyzerAgent (CORE)

    Analisi statica e semantica di:
    - testo
    - codice
    - log

    NON esegue azioni.
    """

    spec = AgentSpec(
        name="analyzer",
        description="Generic analyzer for text, code and logs.",
        domains={"code", "logs", "text"},
        is_observer=True,
        capabilities={
            "analyze.text",
            "analyze.code",
            "analyze.logs",
        },
        ui_label="Analyzer",
        ui_group="core",
    )

    def analyze(
        self,
        content: str,
        mode: str = "auto",
    ) -> Dict[str, Any]:
        """
        Analisi minimale, deterministica.
        """
        if not content:
            return {
                "ok": False,
                "reason": "empty content",
            }

        detected_mode = mode
        if mode == "auto":
            if "def " in content or "class " in content:
                detected_mode = "code"
            elif "ERROR" in content or "WARN" in content:
                detected_mode = "logs"
            else:
                detected_mode = "text"

        return {
            "ok": True,
            "mode": detected_mode,
            "length": len(content),
            "summary": f"Analyzed {detected_mode} content.",
        }
