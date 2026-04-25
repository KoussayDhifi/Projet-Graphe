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
    raise NotImplementedError("kruskal() has not been implemented yet.")
