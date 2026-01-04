from __future__ import annotations

"""
Memory Usage Policy — cognitive governance layer.

Questo modulo definisce:
- COME una memoria PUÒ essere usata
- IN QUALI MODALITÀ cognitive
- CON QUALI VINCOLI semantici

⚠️ NON È runtime logic
⚠️ NON esegue operazioni
⚠️ NON accede a storage
⚠️ NON forza decisioni

Serve esclusivamente per:
- validazione cognitiva
- routing
- reasoning supervision
- audit / explainability
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set

from .contracts import MemoryContract, MemoryScope


# ---------------------------------------------------------------------
# MEMORY USAGE MODES (COGNITIVE)
# ---------------------------------------------------------------------

class MemoryUsageMode(str, Enum):
    """
    Modalità semantica di utilizzo di una memoria.

    NON descrive *come* viene caricata,
    ma *perché* viene utilizzata dal sistema.
    """

    READ = "read"
    """
    Consultazione passiva.
    Non influenza decisioni.
    """

    REFERENCE = "reference"
    """
    Citazione esplicita (es. spiegazioni, report).
    """

    REASONING = "reasoning"
    """
    Usata come input per decisioni, pianificazione o routing.

    ⚠️ MODALITÀ AD ALTO RISCHIO
    """

    CONTEXT = "context"
    """
    Inclusa nel contesto LLM (prompting).
    """

    AUDIT = "audit"
    """
    Tracciamento, explainability, debug.
    """


# ---------------------------------------------------------------------
# MEMORY USAGE POLICY (DECLARATIVE)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class MemoryUsagePolicy:
    """
    Regola dichiarativa di utilizzo di una memoria.

    Serve a:
    - validare se un uso è lecito
    - documentare vincoli cognitivi
    - supportare audit e explainability

    NON:
    - muta stato
    - esegue side-effects
    - forza decisioni
    """

    allowed_modes: Set[MemoryUsageMode]

    # -----------------------------------------------------------------
    # RESTRICTIONS
    # -----------------------------------------------------------------

    require_user_visibility: bool = False
    """
    Se True, la memoria deve essere user_visible per poter essere usata.
    """

    forbid_cross_scope: bool = False
    """
    Se True, vieta l'uso della memoria fuori dal suo scope dichiarato.
    """

    require_explicit_reference: bool = False
    """
    Se True, l'uso richiede una citazione esplicita (audit / reference).
    """

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def allows(
        self,
        *,
        contract: MemoryContract,
        mode: MemoryUsageMode,
        target_scope: Optional[MemoryScope] = None,
    ) -> bool:
        """
        Verifica se un certo utilizzo della memoria è consentito.

        Questa funzione:
        - NON prende decisioni
        - NON esegue azioni
        - NON applica policy strategiche

        Si limita a validare la COERENZA cognitiva.
        """

        # Modalità non consentita
        if mode not in self.allowed_modes:
            return False

        # Visibilità utente richiesta
        if self.require_user_visibility and not contract.user_visible:
            return False

        # Divieto di cross-scope
        if self.forbid_cross_scope and target_scope is not None:
            if target_scope != contract.scope:
                return False

        # -------------------------------------------------------------
        # COGNITIVE SAFETY NOTE (NON LOGICA RUNTIME)
        # -------------------------------------------------------------
        #
        # IMPORTANT:
        # MemoryUsageMode.REASONING SHOULD be restricted to
        # system_critical memories by higher-level policy
        # (router / decision layer).
        #
        # This module DOES NOT enforce that rule programmatically
        # to avoid coupling cognition with execution.
        #
        # -------------------------------------------------------------

        return True


# API pubblica del dominio memory
MemoryUsage = MemoryUsagePolicy
