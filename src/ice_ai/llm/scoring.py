from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class CognitiveScore:
    """
    Valutazione cognitiva di un output generato.

    NON misura:
    - token
    - costi
    - performance runtime

    Misura:
    - qualità del ragionamento
    - utilità per il sistema
    - affidabilità percepita
    """

    clarity: float          # chiarezza espositiva
    coherence: float        # coerenza logica interna
    usefulness: float       # utilità pratica per il task
    confidence: float       # sicurezza / assertività controllata
    correctness: float      # plausibilità / correttezza percepita

    notes: Optional[str] = None

    def overall(self) -> float:
        """
        Score aggregato semplice.
        (media aritmetica — policy modificabile)
        """
        return (
            self.clarity
            + self.coherence
            + self.usefulness
            + self.confidence
            + self.correctness
        ) / 5.0

    def to_dict(self) -> Dict[str, object]:
        return {
            "clarity": self.clarity,
            "coherence": self.coherence,
            "usefulness": self.usefulness,
            "confidence": self.confidence,
            "correctness": self.correctness,
            "overall": self.overall(),
            "notes": self.notes,
        }


# ---------------------------------------------------------------------
# PROFILI DI VALUTAZIONE (DICHIARATIVI)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ScoringProfile:
    """
    Profilo di scoring per un contesto cognitivo.

    Serve a:
    - pesare diversamente i criteri
    - confrontare output alternativi
    """

    name: str
    weights: Dict[str, float]
    description: Optional[str] = None

    def score(self, score: CognitiveScore) -> float:
        """
        Calcola lo score pesato secondo il profilo.
        """
        total = 0.0
        weight_sum = 0.0

        for key, weight in self.weights.items():
            value = getattr(score, key, None)
            if value is None:
                continue
            total += value * weight
            weight_sum += weight

        return total / weight_sum if weight_sum > 0 else 0.0


# ---------------------------------------------------------------------
# PROFILI CANONICI
# ---------------------------------------------------------------------

DEFAULT_PROFILE = ScoringProfile(
    name="default",
    description="Profilo bilanciato generico.",
    weights={
        "clarity": 1.0,
        "coherence": 1.0,
        "usefulness": 1.0,
        "confidence": 0.8,
        "correctness": 1.2,
    },
)

PLANNING_PROFILE = ScoringProfile(
    name="planning",
    description="Profilo per piani e workflow.",
    weights={
        "clarity": 1.2,
        "coherence": 1.4,
        "usefulness": 1.3,
        "confidence": 0.6,
        "correctness": 1.0,
    },
)

DIAGNOSTIC_PROFILE = ScoringProfile(
    name="diagnostic",
    description="Profilo per analisi e diagnosi.",
    weights={
        "clarity": 1.0,
        "coherence": 1.3,
        "usefulness": 1.1,
        "confidence": 0.7,
        "correctness": 1.4,
    },
)

GENERATION_PROFILE = ScoringProfile(
    name="generation",
    description="Profilo per output generativi.",
    weights={
        "clarity": 0.9,
        "coherence": 1.0,
        "usefulness": 1.1,
        "confidence": 0.8,
        "correctness": 0.9,
    },
)


# ---------------------------------------------------------------------
# REGISTRO
# ---------------------------------------------------------------------

SCORING_PROFILES: Dict[str, ScoringProfile] = {
    DEFAULT_PROFILE.name: DEFAULT_PROFILE,
    PLANNING_PROFILE.name: PLANNING_PROFILE,
    DIAGNOSTIC_PROFILE.name: DIAGNOSTIC_PROFILE,
    GENERATION_PROFILE.name: GENERATION_PROFILE,
}
