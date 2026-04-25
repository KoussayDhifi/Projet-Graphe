# ============================================================
# algorithms/traversal/dfs.py
# ============================================================

from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.graph import Graph


def dfs(graph: "Graph", source: int) -> List[Dict]:
    """
    Traverse the graph using Depth-First Search (DFS).

    DFS explores as deep as possible along each branch before backtracking.
    It can be implemented recursively or iteratively with an explicit stack.
    DFS is foundational to many other algorithms (topological sort, SCC, etc.).

    Parameters
    ----------
    graph  : Graph  – the input graph (directed or undirected)
    source : int    – the starting node ID

    Returns
    -------
    List[Dict]
        Animation steps following the event protocol.  Expected events:

        - VISIT_NODE     : when a node is first discovered (grey)
        - PROCESS_NODE   : when a node is fully explored (black)
        - TRAVERSE_EDGE  : when DFS descends into a tree edge
        - REJECT_EDGE    : when a back / cross / forward edge is encountered

    Complexity
    ----------
    Time  : O(V + E)
    Space : O(V)  (call stack depth)

    Raises
    ------
    NotImplementedError
        Placeholder — to be implemented by the algorithm team.
    """
    raise NotImplementedError("dfs() has not been implemented yet.")
