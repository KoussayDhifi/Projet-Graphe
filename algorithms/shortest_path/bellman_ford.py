# ============================================================
# algorithms/shortest_path/bellman_ford.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def bellman_ford(graph: "Graph", source: int) -> List[Dict]:
    """
    Compute single-source shortest paths using the Bellman-Ford algorithm.

    Unlike Dijkstra, Bellman-Ford handles graphs with negative edge weights
    and can detect negative-weight cycles.  It relaxes all edges V-1 times,
    then performs one additional pass to check for negative cycles.

    Parameters
    ----------
    graph  : Graph  – the input graph (directed or undirected)
    source : int    – the source node ID

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - RELAX_EDGE   : each time an edge is relaxed (distance updated)
        - REJECT_EDGE  : each time an edge relaxation fails
        - VISIT_NODE   : when a node's distance is first set to a finite value
        - FINAL_PATH   : the final shortest-path result

    Complexity
    ----------
    Time  : O(V × E)
    Space : O(V)

    Notes
    -----
    If a negative cycle is reachable from the source, the implementation
    should include a special event or raise an exception to signal this.

    Raises
    ------
    NotImplementedError
        This function is a placeholder pending algorithm team implementation.
    """
    raise NotImplementedError("bellman_ford() has not been implemented yet.")
