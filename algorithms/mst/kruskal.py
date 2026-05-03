# ============================================================
# algorithms/mst/kruskal.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def kruskal(graph: "Graph", source: int = None) -> List[Dict]:
    """
    Compute a Minimum Spanning Tree using Kruskal's algorithm.

    Kruskal's algorithm sorts all edges by weight, then greedily adds the
    cheapest edge that does not form a cycle (checked via a Union-Find /
    Disjoint Set Union structure).

    Parameters
    ----------
    graph  : Graph       – the input graph (undirected, weighted)
    source : int | None  – unused; accepted for API consistency

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - EXPLORE_EDGE  : when an edge is considered
        - SELECT_EDGE   : when an edge is added to the MST
        - DISCARD_EDGE  : when an edge is rejected (would form a cycle)
        - FINAL_TREE    : at the end, containing all MST edges

    Complexity
    ----------
    Time  : O(E log E)
    Space : O(V)

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    steps: List[Dict] = []

    # Code panel markers (ignored by renderer, used for highlighting)
    steps.append({"type": "code_init"})
    steps.append({"type": "code_sort"})

    parent = {node_id: node_id for node_id in graph.nodes}
    rank = {node_id: 0 for node_id in graph.nodes}

    def find(node_id: int) -> int:
        while parent[node_id] != node_id:
            parent[node_id] = parent[parent[node_id]]
            node_id = parent[node_id]
        return node_id

    def union(left: int, right: int) -> bool:
        root_left = find(left)
        root_right = find(right)
        if root_left == root_right:
            return False
        if rank[root_left] < rank[root_right]:
            parent[root_left] = root_right
        elif rank[root_left] > rank[root_right]:
            parent[root_right] = root_left
        else:
            parent[root_right] = root_left
            rank[root_left] += 1
        return True

    mst_edges: List[tuple] = []

    for src, dest, weight in sorted(graph.edges, key=lambda edge: (edge[2], edge[0], edge[1])):
        steps.append({"type": "explore_edge", "src": src, "dest": dest})
        if union(src, dest):
            mst_edges.append((src, dest))
            steps.append({"type": "select_edge", "src": src, "dest": dest})
        else:
            steps.append({"type": "discard_edge", "src": src, "dest": dest})

    steps.append({"type": "final_tree", "edges": mst_edges})
    return steps
