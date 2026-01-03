from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class CognitiveRole:
    """
    Ruolo cognitivo astratto per ICE-AI.

    Un ruolo definisce:
    - CHI è l'agente a livello cognitivo
    - QUALI responsabilità mentali ha
    - QUALI limiti non deve superare

    NON definisce:
    - logica di esecuzione
    - accesso a strumenti
    - dipendenze runtime
    """

    name: str
    description: str

    # vincoli cognitivi
    can_plan: bool = False
    can_execute: bool = False
    can_observe: bool = False
    can_decide: bool = False
    is_system: bool = False

    # note semantiche opzionali
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": {
                "plan": self.can_plan,
                "execute": self.can_execute,
                "observe": self.can_observe,
                "decide": self.can_decide,
                "system": self.is_system,
            },
            "notes": self.notes,
        }


# ---------------------------------------------------------------------
# RUOLI CANONICI ICE-AI
# ---------------------------------------------------------------------

SYSTEM_ROLE = CognitiveRole(
    name="system",
    description=(
        "Agente cognitivo globale. "
        "Fornisce spiegazioni, diagnostica e coerenza architetturale. "
        "Non esegue azioni operative."
    ),
    can_plan=False,
    can_execute=False,
    can_observe=True,
    can_decide=True,
    is_system=True,
    notes="Usato fuori dai workspace o come supervisore."
)

PLANNER_ROLE = CognitiveRole(
    name="planner",
    description=(
        "Agente di pianificazione. "
        "Scompone obiettivi complessi in passi ordinati e dipendenze."
    ),
    can_plan=True,
    can_execute=False,
    can_observe=True,
    can_decide=False,
)

ANALYZER_ROLE = CognitiveRole(
    name="analyzer",
    description=(
        "Agente di analisi. "
        "Ispeziona input, codice, log o dati e ne spiega struttura e significato."
    ),
    can_plan=False,
    can_execute=False,
    can_observe=True,
    can_decide=False,
)

VALIDATOR_ROLE = CognitiveRole(
    name="validator",
    description=(
        "Agente di validazione. "
        "Controlla correttezza, coerenza e completezza di risultati o piani."
    ),
    can_plan=False,
    can_execute=False,
    can_observe=True,
    can_decide=True,
)

EXECUTOR_ROLE = CognitiveRole(
    name="executor",
    description=(
        "Agente esecutivo. "
        "Applica azioni decise da altri agenti. "
        "Non prende decisioni strategiche."
    ),
    can_plan=False,
    can_execute=True,
    can_observe=False,
    can_decide=False,
)

OBSERVER_ROLE = CognitiveRole(
    name="observer",
    description=(
        "Agente osservatore. "
        "Raccoglie eventi, segnali e stati senza intervenire."
    ),
    can_plan=False,
    can_execute=False,
    can_observe=True,
    can_decide=False,
)


# ---------------------------------------------------------------------
# REGISTRO DICHIARATIVO
# ---------------------------------------------------------------------

ROLE_REGISTRY: Dict[str, CognitiveRole] = {
    SYSTEM_ROLE.name: SYSTEM_ROLE,
    PLANNER_ROLE.name: PLANNER_ROLE,
    ANALYZER_ROLE.name: ANALYZER_ROLE,
    VALIDATOR_ROLE.name: VALIDATOR_ROLE,
    EXECUTOR_ROLE.name: EXECUTOR_ROLE,
    OBSERVER_ROLE.name: OBSERVER_ROLE,
}
