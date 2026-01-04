from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ice_ai.agents.spec import AgentSpec


# ============================================================
# LOG EVENT MODEL
# ============================================================

@dataclass(frozen=True)
class LogEvent:
    """
    Evento normalizzato prodotto dall'analisi dei log.
    Progettato per:
    - HistorianAgent
    - Timeline
    - UI
    """
    type: str
    message: str
    severity: str = "info"
    file: Optional[str] = None
    line: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "message": self.message,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
        }


# ============================================================
# LOG AGENT
# ============================================================

class LogAgent:
    """
    LogAgent (ICE-AI)

    Responsabilità:
    - Analisi log testuale
    - Detection errori / warning
    - Normalizzazione eventi
    - Output strutturato per Historian

    NON:
    - non modifica filesystem
    - non esegue azioni
    - non dipende da orchestratore
    """

    # --------------------------------------------------------
    # SPEC ICE-AI
    # --------------------------------------------------------

    spec = AgentSpec(
        name="log-agent",
        description="Analisi log, detection anomalie e normalizzazione eventi.",
        domains={"logs"},
        is_observer=True,
        capabilities={
            "logs.analyze",
            "logs.scan_text",
        },
        ui_label="Log Analyzer",
        ui_group="Diagnostics",
    )

    # --------------------------------------------------------
    # ERROR PATTERNS
    # --------------------------------------------------------

    ERROR_PATTERNS = [
        r"\berror\b",
        r"\bexception\b",
        r"\bfail(ed)?\b",
        r"\bfatal\b",
        r"\btraceback\b",
        r"\bpanic\b",
    ]

    WARNING_PATTERNS = [
        r"\bwarn(ing)?\b",
        r"\bdeprecated\b",
        r"\bslow\b",
        r"\bretry\b",
    ]

    MAX_EVENTS = 50

    # ========================================================
    # PUBLIC API
    # ========================================================

    def analyze(
        self,
        log_text: str,
        *,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analizza testo di log grezzo.

        Input:
            log_text: stringa completa log
            source: file / stream / origine opzionale

        Output:
            {
                "events": [...],
                "summary": {...}
            }
        """

        if not log_text.strip():
            return {
                "events": [],
                "summary": {
                    "errors": 0,
                    "warnings": 0,
                    "lines": 0,
                },
            }

        lines = log_text.splitlines()
        events: List[LogEvent] = []

        for idx, line in enumerate(lines, start=1):
            evt = self._analyze_line(
                line=line,
                line_no=idx,
                source=source,
            )
            if evt:
                events.append(evt)
                if len(events) >= self.MAX_EVENTS:
                    break

        summary = {
            "errors": sum(1 for e in events if e.severity == "error"),
            "warnings": sum(1 for e in events if e.severity == "warning"),
            "lines": len(lines),
        }

        return {
            "events": [e.to_dict() for e in events],
            "summary": summary,
        }

    # ========================================================
    # INTERNALS
    # ========================================================

    def _analyze_line(
        self,
        *,
        line: str,
        line_no: int,
        source: Optional[str],
    ) -> Optional[LogEvent]:

        lower = line.lower()

        if self._match(self.ERROR_PATTERNS, lower):
            return LogEvent(
                type="log.error",
                message=line.strip(),
                severity="error",
                file=source,
                line=line_no,
            )

        if self._match(self.WARNING_PATTERNS, lower):
            return LogEvent(
                type="log.warning",
                message=line.strip(),
                severity="warning",
                file=source,
                line=line_no,
            )

        return None

    @staticmethod
    def _match(patterns: List[str], text: str) -> bool:
        for p in patterns:
            if re.search(p, text):
                return True
        return False
