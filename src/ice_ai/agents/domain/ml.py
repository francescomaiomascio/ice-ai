from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ice_ai.agents.spec import AgentSpec


# ============================================================
# ML RESULT MODELS
# ============================================================

@dataclass(frozen=True)
class Anomaly:
    """
    Anomalia rilevata tramite analisi ML/statistica.
    """
    index: int
    score: float
    description: str
    severity: str = "warning"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "score": self.score,
            "description": self.description,
            "severity": self.severity,
        }


# ============================================================
# ML AGENT
# ============================================================

class MLAgent:
    """
    MLAgent (ICE-AI)

    Responsabilità:
    - Analisi ML/statistica su dati testuali o numerici
    - Anomaly detection
    - Pattern discovery (future)
    - Clustering (future)

    NON:
    - non carica modelli pesanti
    - non gestisce training
    - non accede a filesystem
    """

    # --------------------------------------------------------
    # SPEC ICE-AI
    # --------------------------------------------------------

    spec = AgentSpec(
        name="ml-agent",
        description="Analisi ML leggera: anomaly detection e pattern discovery.",
        domains={"ml"},
        is_observer=True,
        capabilities={
            "ml.anomaly.detect",
            "ml.anomaly.score",
        },
        ui_label="ML Analyzer",
        ui_group="Diagnostics",
        experimental=True,
    )

    # ========================================================
    # PUBLIC API
    # ========================================================

    def detect_anomalies(
        self,
        values: List[float] | List[int],
        *,
        z_threshold: float = 3.0,
    ) -> Dict[str, Any]:
        """
        Rileva anomalie tramite z-score (baseline deterministica).

        Input:
            values: lista numerica
            z_threshold: soglia anomalia

        Output:
            {
                "anomalies": [...],
                "summary": {...}
            }
        """

        if not values:
            return {
                "anomalies": [],
                "summary": {
                    "count": 0,
                    "mean": None,
                    "std": None,
                },
            }

        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance ** 0.5

        anomalies: List[Anomaly] = []

        if std == 0:
            return {
                "anomalies": [],
                "summary": {
                    "count": 0,
                    "mean": mean,
                    "std": std,
                },
            }

        for idx, v in enumerate(values):
            z = abs((v - mean) / std)
            if z >= z_threshold:
                anomalies.append(
                    Anomaly(
                        index=idx,
                        score=round(z, 3),
                        description=f"Value {v} deviates from mean",
                        severity="error" if z >= z_threshold * 1.5 else "warning",
                    )
                )

        return {
            "anomalies": [a.to_dict() for a in anomalies],
            "summary": {
                "count": len(anomalies),
                "mean": round(mean, 4),
                "std": round(std, 4),
                "threshold": z_threshold,
            },
        }

    # ========================================================
    # EXTENSION POINTS (FUTURE)
    # ========================================================

    def score_series(self, values: List[float]) -> List[float]:
        """
        Restituisce uno score normalizzato per ogni valore.
        Placeholder per futuri modelli ML.
        """
        if not values:
            return []

        max_v = max(values)
        if max_v == 0:
            return [0.0 for _ in values]

        return [round(v / max_v, 4) for v in values]
