from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


# =====================================================================
# TASK NODE (COGNITIVE UNIT)
# =====================================================================

@dataclass(frozen=True)
class TaskNode:
    """
    Nodo cognitivo di un workflow.

    NON È:
    - un task runtime
    - un job schedulabile
    - un'azione eseguibile

    È:
    - un vincolo logico
    - un'unità di pianificazione
    - un elemento di reasoning

    Serve per:
    - planning
    - routing
    - validazione
    - introspezione
    """

    id: str
    kind: str                     # es: "plan", "analyze", "validate", "refactor"
    description: str

    # Vincoli cognitivi
    required_capabilities: Set[str] = field(default_factory=set)
    suggested_agent: Optional[str] = None

    # Metadati puramente semantici (mai runtime)
    metadata: Dict[str, object] = field(default_factory=dict)

    # -------------------------------------------------------------

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "kind": self.kind,
            "description": self.description,
            "required_capabilities": sorted(self.required_capabilities),
            "suggested_agent": self.suggested_agent,
            "metadata": dict(self.metadata),
        }


# =====================================================================
# TASK GRAPH (PURE DAG)
# =====================================================================

@dataclass
class TaskGraph:
    """
    Grafo diretto aciclico (DAG) di TaskNode.

    PROPRIETÀ FONDAMENTALI:
    - puramente cognitivo
    - deterministico
    - serializzabile
    - validabile

    NON CONOSCE:
    - AgentRunner
    - Scheduler
    - Session
    - Stato di esecuzione
    """

    nodes: Dict[str, TaskNode] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)  # from -> [to]

    # ------------------------------------------------------------
    # NODE MANAGEMENT
    # ------------------------------------------------------------

    def add_node(self, node: TaskNode) -> None:
        if node.id in self.nodes:
            raise ValueError(f"TaskNode already exists: {node.id}")

        self.nodes[node.id] = node
        self.edges.setdefault(node.id, [])

    def get_node(self, node_id: str) -> TaskNode:
        try:
            return self.nodes[node_id]
        except KeyError:
            raise KeyError(f"TaskNode not found: {node_id}")

    # ------------------------------------------------------------
    # DEPENDENCIES
    # ------------------------------------------------------------

    def add_dependency(self, before: str, after: str) -> None:
        """
        Registra una dipendenza logica:
            before → after
        """
        if before not in self.nodes:
            raise ValueError(f"Unknown node: {before}")
        if after not in self.nodes:
            raise ValueError(f"Unknown node: {after}")

        self.edges.setdefault(before, []).append(after)

    def dependencies_of(self, node_id: str) -> List[str]:
        """
        Nodi che devono essere completati PRIMA di node_id.
        """
        return [
            src for src, targets in self.edges.items()
            if node_id in targets
        ]

    def dependents_of(self, node_id: str) -> List[str]:
        """
        Nodi che dipendono da node_id.
        """
        return list(self.edges.get(node_id, []))

    # ------------------------------------------------------------
    # GRAPH INTROSPECTION
    # ------------------------------------------------------------

    def roots(self) -> List[str]:
        """
        Nodi senza dipendenze in ingresso.
        """
        return [
            node_id
            for node_id in self.nodes
            if not self.dependencies_of(node_id)
        ]

    def leaves(self) -> List[str]:
        """
        Nodi senza dipendenze in uscita.
        """
        return [
            node_id
            for node_id, targets in self.edges.items()
            if not targets
        ]

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------

    def is_valid_dag(self) -> bool:
        """
        Verifica che il grafo sia aciclico.
        """
        visited: Set[str] = set()
        stack: Set[str] = set()

        def visit(node_id: str) -> bool:
            if node_id in stack:
                return False
            if node_id in visited:
                return True

            stack.add(node_id)
            for nxt in self.edges.get(node_id, []):
                if not visit(nxt):
                    return False
            stack.remove(node_id)
            visited.add(node_id)
            return True

        return all(visit(n) for n in self.nodes)

    # ------------------------------------------------------------
    # SERIALIZATION
    # ------------------------------------------------------------

    def to_dict(self) -> Dict[str, object]:
        return {
            "nodes": {
                node_id: node.to_dict()
                for node_id, node in self.nodes.items()
            },
            "edges": {
                src: list(targets)
                for src, targets in self.edges.items()
            },
            "roots": self.roots(),
            "leaves": self.leaves(),
            "valid_dag": self.is_valid_dag(),
        }
