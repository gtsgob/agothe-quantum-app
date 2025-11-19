"""
constraint_graph.py

This module constructs and updates a constraint graph representing relationships among Agothean constraints, resonance terms, collapse metrics, and other variables.
It uses a simple adjacency list to avoid heavy dependencies. Each node is a concept, such as 'LSSE', 'delta_H', 'Orric', 'Resonance', 'CivilizationLevel', etc.
Edges encode interactions between constraints and are annotated with relation labels like 'implies', 'increases', 'decreases', or 'causes'.

This skeleton is intentionally simple; no dynamic inference or external dependencies are used. It can be extended to use networkx or other graph libraries later.
"""

from typing import Dict, List, Any, Tuple
import json
import os

class ConstraintGraph:
    """A simple directed graph structure for constraints."""
    def __init__(self) -> None:
        # adjacency list: node -> list of (target, relation)
        self.graph: Dict[str, List[Tuple[str, str]]] = {}

    def add_node(self, node: str) -> None:
        """Ensure a node exists in the graph."""
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, source: str, target: str, relation: str) -> None:
        """Add a directed edge with a relation label."""
        self.add_node(source)
        self.add_node(target)
        self.graph[source].append((target, relation))

    def update_from_constraints(self, constraints: List[Dict[str, Any]]) -> None:
        """
        Update the graph based on a list of constraint entries extracted from the corpus.
        Each constraint dict may contain 'type', 'content', or other metadata.
        This placeholder uses simple heuristics: equations containing '=' produce edges between left and right terms with an 'implies' relation.
        """
        for constraint in constraints:
            text = constraint.get("content", "")
            if constraint.get("type") == "equation" and "=" in text:
                lhs, rhs = map(str.strip, text.split("=", 1))
                self.add_edge(lhs, rhs, "implies")

    def merge(self, other: 'ConstraintGraph') -> None:
        """Merge another ConstraintGraph into this one."""
        for node, edges in other.graph.items():
            for tgt, rel in edges:
                self.add_edge(node, tgt, rel)

    def serialize(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation of the graph."""
        return {node: [{"target": tgt, "relation": rel} for tgt, rel in edges] for node, edges in self.graph.items()}

    def save(self, path: str) -> None:
        """Save the serialized graph to a JSON file."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.serialize(), f, indent=2)


def build_graph_from_corpus(corpus_path: str) -> ConstraintGraph:
    """
    Build a ConstraintGraph from a corpus.json file produced by corpus_ingestor.
    """
    graph = ConstraintGraph()
    if not os.path.isfile(corpus_path):
        return graph
    with open(corpus_path) as f:
        data = json.load(f)
    # data expected to be { filename: [entries...] }
    for entries in data.values():
        graph.update_from_constraints(entries)
    return graph


if __name__ == "__main__":
    # Determine corpus input and graph output paths from environment variables
    corpus_path = os.environ.get("AGOTHE_CORPUS_JSON", "./state/corpus.json")
    graph_output = os.environ.get("AGOTHE_GRAPH_OUTPUT", "./knowledge_graph/constraint_graph.json")
    cg = build_graph_from_corpus(corpus_path)
    cg.save(graph_output)
    print(f"Constraint graph built from {corpus_path} and saved to {graph_output}")
