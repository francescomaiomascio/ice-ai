from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Set


class MemoryScope(str, Enum):
    """
    Ambito logico della memoria.

    NON è uno scope tecnico (db, cache, ecc.),
    ma cognitivo/semantico.
    """

    GLOBAL = "global"          # conoscenza generale del sistema
    WORKSPACE = "workspace"    # legata a uno specifico workspace
    SESSION = "session"        # valida solo per una sessione attiva
    TASK = "task"              # valida solo per un singolo task


class MemoryKind(str, Enum):
    """
    Tipologia semantica del contenuto memorizzato.
    """

    FACT = "fact"                  # fatto verificabile
    DECISION = "decision"          # scelta presa dal sistema
    PLAN = "plan"                  # piano generato
    SUMMARY = "summary"            # riassunto
    CODE_CHANGE = "code_change"    # modifica o refactor
    EVENT = "event"                # evento rilevante
    NOTE = "note"                  # annotazione non strutturata


@dataclass(frozen=True)
class MemoryContract:
    """
    Contratto dichiarativo di una memoria.

    Definisce:
    - COSA può essere ricordato
    - PER QUANTO è valido
    - IN CHE CONTESTO è lecito usarlo

    NON definisce:
    - storage
    - serializzazione
    - backend
    """

    name: str
    description: str

    kind: MemoryKind
    scope: MemoryScope

    # Governance
    mutable: bool = False          # può essere aggiornato?
    expires: bool = False          # ha una scadenza?
    user_visible: bool = False     # mostrabile in UI?
    system_critical: bool = False  # influisce su decisioni core?

    # Tag liberi (routing, policy, introspezione)
    tags: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "kind": self.kind.value,
            "scope": self.scope.value,
            "mutable": self.mutable,
            "expires": self.expires,
            "user_visible": self.user_visible,
            "system_critical": self.system_critical,
            "tags": sorted(self.tags),
        }
