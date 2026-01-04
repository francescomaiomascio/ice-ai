from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class CognitiveMode:
    """
    Modalità cognitiva astratta.

    Un mode definisce:
    - COME l'agente deve ragionare
    - QUALE tipo di output produrre
    - QUALI trade-off privilegiare

    NON definisce:
    - ruolo (chi sei)
    - capacità (cosa puoi fare)
    - runtime (come esegui)
    """

    name: str
    description: str

    # caratteristiche cognitive
    structured: bool = False        # output strutturato (JSON, liste, DAG)
    exploratory: bool = False       # esplorazione ampia, ipotesi multiple
    deterministic: bool = False     # preferisci stabilità a creatività
    critical: bool = False          # cerca errori, incoerenze
    generative: bool = False        # produce nuovi contenuti
    summarizing: bool = False       # riduce e distilla informazione

    # hint semantico opzionale
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "traits": {
                "structured": self.structured,
                "exploratory": self.exploratory,
                "deterministic": self.deterministic,
                "critical": self.critical,
                "generative": self.generative,
                "summarizing": self.summarizing,
            },
            "notes": self.notes,
        }


# alias semantico pubblico
LLMMode = CognitiveMode


# ---------------------------------------------------------------------
# MODI COGNITIVI CANONICI
# ---------------------------------------------------------------------

EXPLAIN_MODE = CognitiveMode(
    name="explain",
    description=(
        "Spiegazione chiara e lineare di concetti, sistemi o comportamenti."
    ),
    structured=False,
    exploratory=False,
    deterministic=True,
    summarizing=False,
)

DIAGNOSE_MODE = CognitiveMode(
    name="diagnose",
    description=(
        "Analisi critica orientata all'individuazione di problemi e cause radice."
    ),
    structured=True,
    critical=True,
    deterministic=True,
)

PLAN_MODE = CognitiveMode(
    name="plan",
    description=(
        "Produzione di piani ordinati, passi sequenziali o grafi di task."
    ),
    structured=True,
    deterministic=True,
    notes="Tipicamente usato con ruoli planner.",
)

DECIDE_MODE = CognitiveMode(
    name="decide",
    description=(
        "Valutazione di alternative e selezione della migliore opzione."
    ),
    structured=True,
    critical=True,
    deterministic=True,
)

EXPLORE_MODE = CognitiveMode(
    name="explore",
    description=(
        "Esplorazione ampia di possibilità, idee o ipotesi alternative."
    ),
    exploratory=True,
    generative=True,
    deterministic=False,
)

SUMMARIZE_MODE = CognitiveMode(
    name="summarize",
    description=(
        "Riduzione e distillazione dell'informazione essenziale."
    ),
    summarizing=True,
    deterministic=True,
)

GENERATE_MODE = CognitiveMode(
    name="generate",
    description=(
        "Generazione di nuovi contenuti: testo, codice, strutture."
    ),
    generative=True,
    exploratory=True,
    deterministic=False,
)


# ---------------------------------------------------------------------
# REGISTRO DICHIARATIVO
# ---------------------------------------------------------------------

MODE_REGISTRY: Dict[str, CognitiveMode] = {
    EXPLAIN_MODE.name: EXPLAIN_MODE,
    DIAGNOSE_MODE.name: DIAGNOSE_MODE,
    PLAN_MODE.name: PLAN_MODE,
    DECIDE_MODE.name: DECIDE_MODE,
    EXPLORE_MODE.name: EXPLORE_MODE,
    SUMMARIZE_MODE.name: SUMMARIZE_MODE,
    GENERATE_MODE.name: GENERATE_MODE,
}
