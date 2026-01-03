from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set

from .contracts import MemoryContract, MemoryScope


class MemoryUsageMode(str, Enum):
    """
    Modalità di utilizzo di una memoria.
    """

    READ = "read"              # consultazione
    REFERENCE = "reference"    # citazione esplicita
    REASONING = "reasoning"    # usata per decisioni/pianificazione
    CONTEXT = "context"        # inclusa nel prompt / contesto
    AUDIT = "audit"            # tracciamento / explainability


@dataclass(frozen=True)
class MemoryUsagePolicy:
    """
    Regola dichiarativa di utilizzo di una memoria.

    Serve a:
    - validare l'uso da parte di agenti
    - guidare reasoning e routing
    - spiegare decisioni (audit)
    """

    allowed_modes: Set[MemoryUsageMode]

    # Restrizioni opzionali
    require_user_visibility: bool = False
    forbid_cross_scope: bool = False   # es: session -> global
    require_explicit_reference: bool = False

    def allows(
        self,
        *,
        contract: MemoryContract,
        mode: MemoryUsageMode,
        target_scope: Optional[MemoryScope] = None,
    ) -> bool:
        """
        Verifica se un certo uso è consentito secondo la policy.
        """

        if mode not in self.allowed_modes:
            return False

        if self.require_user_visibility and not contract.user_visible:
            return False

        if self.forbid_cross_scope and target_scope:
            if target_scope != contract.scope:
                return False

        return True
