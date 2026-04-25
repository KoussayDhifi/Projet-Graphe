# ============================================================
# core/graph.py — Core graph data structure
# ============================================================

from __future__ import annotations
from typing import Dict, List, Tuple


class Graph:
    """
    Core graph representation used throughout the application.

    Attributes
    ----------
    nodes    : Dict[int, Tuple[int, int]]
        Maps node ID → (x, y) screen coordinates.
    edges    : List[Tuple[int, int, float]]
        Each edge is (src, dest, weight).
    directed : bool
        Whether the graph is directed.
    weighted : bool
        Whether edge weights are meaningful.
    """

    def __init__(self, directed: bool = False, weighted: bool = False) -> None:
        self.nodes: Dict[int, Tuple[int, int]] = {}
        self.edges: List[Tuple[int, int, float]] = []
        self.directed: bool = directed
        self.weighted: bool = weighted
        self._next_id: int = 0

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_node(self, x: int, y: int) -> int:
        """
        Add a node at screen position (x, y).

        Returns
        -------
        int
            The new node's sequential ID (0-indexed).
        """
        node_id = self._next_id
        self.nodes[node_id] = (x, y)
        self._next_id += 1
        return node_id

    def add_edge(self, src: int, dest: int, weight: float = 1.0) -> None:
        """
        Add an edge between src and dest.

        For undirected graphs both (src→dest) and (dest→src) are stored
        so that adjacency queries work uniformly in both directions.

        Parameters
        ----------
        src    : int   – source node ID
        dest   : int   – destination node ID
        weight : float – edge weight (default 1.0)
        """
        if src not in self.nodes or dest not in self.nodes:
            raise ValueError(f"Node {src} or {dest} does not exist.")
        if src == dest:
            raise ValueError("Self-loops are not supported.")

        # Avoid duplicate edges
        for s, d, _ in self.edges:
            if s == src and d == dest:
                return
            if not self.directed and s == dest and d == src:
                return

        self.edges.append((src, dest, weight))

    def remove_node(self, node_id: int) -> None:
        """Remove a node and all edges incident to it."""
        if node_id not in self.nodes:
            raise KeyError(f"Node {node_id} not found.")
        del self.nodes[node_id]
        self.edges = [
            (s, d, w) for s, d, w in self.edges
            if s != node_id and d != node_id
        ]

    def remove_edge(self, src: int, dest: int) -> None:
        """Remove an edge (and its reverse for undirected graphs)."""
        self.edges = [
            (s, d, w) for s, d, w in self.edges
            if not ((s == src and d == dest) or
                    (not self.directed and s == dest and d == src))
        ]

    def clear(self) -> None:
        """Reset the graph to an empty state."""
        self.nodes.clear()
        self.edges.clear()
        self._next_id = 0

    # ------------------------------------------------------------------
    # Representations
    # ------------------------------------------------------------------

    def to_matrix(self) -> List[List[float]]:
        """
        Build an adjacency matrix of size n×n.

        Missing edges are represented as float('inf').
        Self entries are 0.
        """
        n = len(self.nodes)
        # Map node IDs to 0..n-1 indices in insertion order
        id_to_idx = {nid: i for i, nid in enumerate(sorted(self.nodes))}
        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0.0
        for src, dest, weight in self.edges:
            i, j = id_to_idx[src], id_to_idx[dest]
            matrix[i][j] = weight
            if not self.directed:
                matrix[j][i] = weight
        return matrix

    def to_adj_list(self) -> Dict[int, List[Tuple[int, float]]]:
        """
        Build an adjacency list.

        Returns
        -------
        Dict[int, List[Tuple[int, float]]]
            node_id → [(neighbor_id, weight), ...]
        """
        adj: Dict[int, List[Tuple[int, float]]] = {nid: [] for nid in self.nodes}
        for src, dest, weight in self.edges:
            adj[src].append((dest, weight))
            if not self.directed:
                adj[dest].append((src, weight))
        return adj

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def node_count(self) -> int:
        return len(self.nodes)

    def edge_count(self) -> int:
        return len(self.edges)

    def neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        """Return [(neighbor, weight)] for a given node."""
        return self.to_adj_list().get(node_id, [])

    def has_edge(self, src: int, dest: int) -> bool:
        for s, d, _ in self.edges:
            if s == src and d == dest:
                return True
            if not self.directed and s == dest and d == src:
                return True
        return False

    def get_edge_weight(self, src: int, dest: int) -> float:
        for s, d, w in self.edges:
            if s == src and d == dest:
                return w
            if not self.directed and s == dest and d == src:
                return w
        return float('inf')

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Graph(nodes={self.node_count()}, edges={self.edge_count()}, "
            f"directed={self.directed}, weighted={self.weighted})"
        )
