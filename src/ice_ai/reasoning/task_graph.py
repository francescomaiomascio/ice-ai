from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


# ---------------------------------------------------------
# TASK NODE
# ---------------------------------------------------------

@dataclass(frozen=True)
class TaskNode:
    """
    Nodo logico di un workflow cognitivo.

    NON è un task runtime.
    NON contiene stato di esecuzione.
    Serve per:
    - planning
    - reasoning
    - validazione
    """

    id: str
    kind: str                # es: "analyze", "plan", "refactor"
    description: str

    # Vincoli logici
    required_capabilities: Set[str] = field(default_factory=set)
    suggested_agent: Optional[str] = None

    # Metadati puramente cognitivi
    metadata: Dict[str, object] = field(default_factory=dict)


# ---------------------------------------------------------
# TASK GRAPH
# ---------------------------------------------------------

@dataclass
class TaskGraph:
    """
    Grafo diretto aciclico (DAG) di TaskNode.

    NON conosce:
    - AgentRunner
    - Scheduler
    - Session
    """

    nodes: Dict[str, TaskNode] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)  # from -> [to]

    def add_node(self, node: TaskNode) -> None:
        self.nodes[node.id] = node
        self.edges.setdefault(node.id, [])

    def add_dependency(self, before: str, after: str) -> None:
        if before not in self.nodes or after not in self.nodes:
            raise ValueError("Both nodes must exist in graph")
        self.edges.setdefault(before, []).append(after)

    def dependencies_of(self, node_id: str) -> List[str]:
        return [
            src for src, targets in self.edges.items()
            if node_id in targets
        ]

    def is_valid_dag(self) -> bool:
        """
        Verifica assenza di cicli.
        """
        visited = set()
        stack = set()

        def visit(n: str) -> bool:
            if n in stack:
                return False
            if n in visited:
                return True
            stack.add(n)
            for m in self.edges.get(n, []):
                if not visit(m):
                    return False
            stack.remove(n)
            visited.add(n)
            return True

        return all(visit(n) for n in self.nodes)
