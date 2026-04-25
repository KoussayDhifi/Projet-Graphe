# ============================================================
# algorithms/shortest_path/dijkstra.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def dijkstra(graph: "Graph", source: int) -> List[Dict]:
    """
    Compute single-source shortest paths using Dijkstra's algorithm.

    Dijkstra's algorithm works on graphs with non-negative edge weights.
    It maintains a priority queue (min-heap) ordered by tentative distance
    and greedily settles nodes in order of increasing distance from the source.

    Parameters
    ----------
    graph  : Graph  – the input graph (directed or undirected, weighted)
    source : int    – the source node ID

    Returns
    -------
    List[Dict]
        A sequence of animation steps following the event protocol defined
        in ``animation/events.py``.  Expected event types:

        - VISIT_NODE      : when a node is extracted from the priority queue
        - RELAX_EDGE      : when a shorter path to a neighbour is found
        - EXPLORE_EDGE    : when an edge is examined
        - REJECT_EDGE     : when an edge does not improve the distance
        - PROCESS_NODE    : when a node's distance is finalised
        - FINAL_PATH      : at the end, highlighting the shortest path tree

    Complexity
    ----------
    Time  : O((V + E) log V) with a binary heap
    Space : O(V)

    Raises
    ------
    NotImplementedError
        This function is a placeholder; implementation is delegated to
        the algorithm team.
    """
    raise NotImplementedError("dijkstra() has not been implemented yet.")
