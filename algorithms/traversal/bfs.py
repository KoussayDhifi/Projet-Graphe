# ============================================================
# algorithms/traversal/bfs.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def bfs(graph: "Graph", source: int) -> List[Dict]:
    """
    Traverse the graph using Breadth-First Search (BFS).

    BFS explores nodes level by level, visiting all neighbours of the
    current node before moving to the next level.  It uses a FIFO queue.
    BFS produces a BFS tree and can be used to find shortest paths in
    unweighted graphs.

    Parameters
    ----------
    graph  : Graph  – the input graph (directed or undirected)
    source : int    – the starting node ID

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - VISIT_NODE     : when a node is enqueued for the first time
        - PROCESS_NODE   : when a node is dequeued and processed
        - TRAVERSE_EDGE  : when the BFS moves along a tree edge
        - REJECT_EDGE    : when a cross / back edge is encountered

    Complexity
    ----------
    Time  : O(V + E)
    Space : O(V)

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    raise NotImplementedError("bfs() has not been implemented yet.")
