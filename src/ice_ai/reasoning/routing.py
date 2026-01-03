from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------
# ROUTING DECISION
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RoutingDecision:
    """
    Decisione cognitiva su cosa fare dopo.

    NON è un'azione runtime.
    È una direttiva logica per il sistema.
    """

    kind: str
    """
    Tipo di decisione, es:
    - "respond"
    - "plan"
    - "analyze"
    - "validate"
    """

    reason: str
    """
    Motivazione semantica della decisione.
    """

    payload: Dict[str, Any] = None
    """
    Dati utili per lo step successivo
    (goal, raw_actions, query, ecc.)
    """

    next_roles: Optional[List[str]] = None
    """
    Ruoli suggeriti (planner, analyzer, validator, ecc.)
    """


# ---------------------------------------------------------------------
# ROUTER LOGIC (PURE)
# ---------------------------------------------------------------------

class Router:
    """
    Logica pura di routing cognitivo.

    Decide cosa fare DOPO una risposta o un reasoning.
    """

    @staticmethod
    def route(
        *,
        user_query: str,
        llm_output: Optional[Dict[str, Any]] = None,
        mode: Optional[str] = None,
    ) -> RoutingDecision:
        """
        Decide il prossimo passo logico.

        Parametri:
        - user_query: input originale dell'utente
        - llm_output: output grezzo del modello (se esiste)
        - mode: hint esplicito (es. "plan", "explain")
        """

        # -------------------------------------------------------------
        # MODE OVERRIDE (esplicito)
        # -------------------------------------------------------------

        if mode == "plan":
            return RoutingDecision(
                kind="plan",
                reason="Explicit planning mode requested.",
                payload={
                    "goal": user_query,
                    "raw_actions": llm_output.get("actions") if llm_output else None,
                },
                next_roles=["planner"],
            )

        if mode == "explain":
            return RoutingDecision(
                kind="respond",
                reason="Explicit explanation mode.",
                payload={
                    "answer": llm_output.get("answer") if llm_output else None,
                },
            )

        # -------------------------------------------------------------
        # HEURISTIC ROUTING
        # -------------------------------------------------------------

        # Se il modello ha prodotto azioni strutturate → pianificazione
        if llm_output and llm_output.get("actions"):
            return RoutingDecision(
                kind="plan",
                reason="LLM produced structured actions.",
                payload={
                    "goal": user_query,
                    "raw_actions": llm_output.get("actions"),
                },
                next_roles=["planner"],
            )

        # Se contiene errori / warning → validazione
        if llm_output and llm_output.get("issues"):
            return RoutingDecision(
                kind="validate",
                reason="Potential issues detected.",
                payload={
                    "issues": llm_output.get("issues"),
                },
                next_roles=["validator"],
            )

        # Default: risposta diretta
        return RoutingDecision(
            kind="respond",
            reason="No further processing required.",
            payload={
                "answer": llm_output.get("answer") if llm_output else None,
            },
        )
