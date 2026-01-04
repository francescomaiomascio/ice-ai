from __future__ import annotations

"""
Agent Capabilities — vocabolario e profilo dichiarativo ICE-AI.

Questo modulo definisce:
- il vocabolario canonico delle capability
- il profilo dichiarativo di un agente
- helper per routing / planning / introspezione

NON contiene:
- logica runtime
- dipendenze engine
- istanziazione
"""

from dataclasses import dataclass, field
from typing import Set, Dict, Any, Iterable


# =====================================================================
# CAPABILITY VOCABULARY (CANONICAL)
# =====================================================================

class Capability:
    """
    Vocabolario canonico delle capability ICE-AI.

    USARE SOLO QUESTE STRINGHE.
    Vietato inventarne altre nei file agent.
    """

    # --- Code / Dev ---
    CODE_READ = "code.read"
    CODE_WRITE = "code.write"
    CODE_GENERATE = "code.generate"
    CODE_REFACTOR = "code.refactor"
    CODE_VALIDATE = "code.validate"
    CODE_SCAN = "code.scan"

    # --- Git ---
    GIT_STATUS = "git.status"
    GIT_DIFF = "git.diff"
    GIT_COMMIT = "git.commit"
    GIT_CHECKOUT = "git.checkout"
    GIT_LOG = "git.log"
    GIT_BRANCHES = "git.branches"

    # --- Logs / Analysis ---
    LOG_ANALYZE = "log.analyze"
    LOG_SCAN = "log.scan"
    ANOMALY_DETECT = "ml.anomaly.detect"

    # --- Knowledge / RAG ---
    RAG_INGEST = "rag.ingest"
    RAG_QUERY = "rag.query"
    KNOWLEDGE_SYNC = "knowledge.sync"
    KNOWLEDGE_QUERY = "knowledge.query"

    # --- Planning / Workflow ---
    WORKFLOW_PLAN = "workflow.plan"
    WORKFLOW_ROUTE = "workflow.route"
    WORKFLOW_VALIDATE = "workflow.validate"

    # --- Project ---
    PROJECT_GENERATE = "project.generate"

    # --- CV ---
    CV_PARSE = "cv.parse"
    CV_RENDER = "cv.render"
    CV_EXPORT = "cv.export"

    # --- System ---
    SYSTEM_BOOT = "system.boot"
    SYSTEM_INTROSPECT = "system.introspect"


# =====================================================================
# AGENT CAPABILITY PROFILE
# =====================================================================

@dataclass(frozen=True)
class AgentCapabilities:
    """
    Profilo dichiarativo delle capacità di un agente.

    È:
    - immutabile
    - serializzabile
    - usato da planner / router / UI

    NON contiene logica.
    """

    # -------------------------------------------------
    # RUOLI LOGICI
    # -------------------------------------------------

    is_planner: bool = False
    is_executor: bool = False
    is_observer: bool = False
    is_system: bool = False

    # -------------------------------------------------
    # DIPENDENZE FUNZIONALI
    # -------------------------------------------------

    uses_llm: bool = False
    uses_internal_codemodel: bool = False
    uses_knowledge: bool = False

    # -------------------------------------------------
    # GOVERNANCE
    # -------------------------------------------------

    experimental: bool = False
    deprecated: bool = False

    # -------------------------------------------------
    # CAPABILITY SEMANTICHE
    # -------------------------------------------------

    capabilities: Set[str] = field(default_factory=set)

    # -------------------------------------------------
    # API
    # -------------------------------------------------

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    def supports_any(self, caps: Iterable[str]) -> bool:
        return any(c in self.capabilities for c in caps)

    def supports_all(self, caps: Iterable[str]) -> bool:
        return all(c in self.capabilities for c in caps)

    def with_capabilities(self, *caps: str) -> "AgentCapabilities":
        """
        Ritorna una nuova istanza con capability aggiunte.
        """
        return AgentCapabilities(
            is_planner=self.is_planner,
            is_executor=self.is_executor,
            is_observer=self.is_observer,
            is_system=self.is_system,
            uses_llm=self.uses_llm,
            uses_internal_codemodel=self.uses_internal_codemodel,
            uses_knowledge=self.uses_knowledge,
            experimental=self.experimental,
            deprecated=self.deprecated,
            capabilities=self.capabilities.union(caps),
        )

    # -------------------------------------------------
    # SERIALIZATION
    # -------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "roles": {
                "planner": self.is_planner,
                "executor": self.is_executor,
                "observer": self.is_observer,
                "system": self.is_system,
            },
            "dependencies": {
                "llm": self.uses_llm,
                "internal_codemodel": self.uses_internal_codemodel,
                "knowledge": self.uses_knowledge,
            },
            "flags": {
                "experimental": self.experimental,
                "deprecated": self.deprecated,
            },
            "capabilities": sorted(self.capabilities),
        }
    
    def with_capability(self, cap: str) -> "AgentCapabilities":
        """
        Return a new AgentCapabilities with a single capability added.
        Convenience wrapper around with_capabilities().
        """
        return self.with_capabilities(cap)

